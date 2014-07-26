#!/usr/bin/evn python

import pydot

# Import pygraph
from dionysus_dependency_graph import dionysus_dependency_graph
from dionysus_algorithms import *
from pygraph.readwrite.dot import write

def create_FR_case_dependency_graph():
	gr = dionysus_dependency_graph()
	# add operation
	gr.add_operation_node("s8")
	gr.add_operation_node("s7")
	gr.add_operation_node("s6")
	gr.add_operation_node("s5_1")
	gr.add_operation_node("s5_2")

	gr.add_operation_node("s4")
	gr.add_operation_node("s3")
	gr.add_operation_node("s2")
	gr.add_operation_node("s1")

	gr.add_resource_node("s6-s5")
	gr.add_resource_node("s4-s5")
	gr.add_resource_node("s3-s4")
	gr.add_resource_node("s4-s7")
	gr.add_resource_node("s1-s8", 0, -5)

	gr.add_edge(("s7", "s8"), 0)
	gr.add_edge(("s5_1", "s8"), 0)
	gr.add_edge(("s8", "s6"), 0)
	gr.add_edge(("s8", "s5_2"), 0)

	gr.add_edge(("s8", "s6-s5"), 5)
	gr.add_edge(("s6-s5", "s3"), 5)
	gr.add_edge(("s3", "s4-s5"), 5)
	gr.add_edge(("s3", "s3-s4"), 5)
	gr.add_edge(("s3-s4", "s1"), 5)
	gr.add_edge(("s4-s5", "s4"), 5)
	gr.add_edge(("s1", "s1-s8"), 5)
	gr.add_edge(("s4", "s4-s7"), 5)
	gr.add_edge(("s4-s7", "s1"), 5)
	gr.add_edge(("s2", "s4-s5"), 5)

	dot = write(gr)
	graph = pydot.graph_from_dot_data(dot)
	graph.write_png('FR_case.png')

	return gr

def test_dependency_graph(graph):

	graph.print_all()

	print "*** s8's incidents(parents) ***"
	for each in graph.incidents("s8"):
		print each

	print "*** s8's neighbors(children) ***"
	for each in graph.neighbors("s8"):
		print each

	cpl_list = critial_path_length_list(graph)

	print "*** node in its cpl's decreasing order ***"
	for each in cpl_list:
		print "node & its cpl: " + str(each)
		graph.set_scheduled(each[0])

	graph.print_all()

	graph.del_node("s8")

	graph.print_all()



def main():
	graph = create_FR_case_dependency_graph()
	test_dependency_graph(graph)


if __name__ == "__main__":
	main()








