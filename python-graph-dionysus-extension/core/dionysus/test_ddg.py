#!/usr/bin/evn python

import pydot

# Import pygraph
from dionysus_dependency_graph import dionysus_dependency_graph
from dionysus_algorithms import *
from pygraph.readwrite.dot import write

import unittest

def create_FR_case_dependency_graph():
	gr = dionysus_dependency_graph()

	gr.add_operation_node("s8", 1, True, "del_tunnel")
	gr.add_operation_node("s7")
	gr.add_operation_node("s6", 1, True, "chg_weight")
	gr.add_operation_node("s5_1")
	gr.add_operation_node("s5_2", 1, True, "del_tunnel")

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

class TestDDGFunctions(unittest.TestCase):
	"""use unittest framework testing dionysus_dependency_graph"""
	def setUp(self):
		self.graph = create_FR_case_dependency_graph()

	def test_incidents(self):
		self.assertItemsEqual(self.graph.incidents("s8"), ["s5_1", "s7"])

	def test_neighbors(self):
		self.assertItemsEqual(self.graph.neighbors("s8"), ["s6", "s5_2", "s6-s5"])

	def test_is_add_tunnel_operation(self):
		self.assertFalse(self.graph.is_add_tunnel_operation("s8"))
		self.assertTrue(self.graph.is_add_tunnel_operation("s7"))

	def test_is_del_tunnel_operation(self):
		self.assertTrue(self.graph.is_del_tunnel_operation("s8"))
		self.assertFalse(self.graph.is_del_tunnel_operation("s3"))

	def test_is_chg_weight_operation(self):
		self.assertTrue(self.graph.is_chg_weight_operation("s6"))
		self.assertFalse(self.graph.is_chg_weight_operation("s3"))

	def test_has_operation_parents(self):
		self.assertTrue(self.graph.has_operation_parents("s1-s8"))
		self.assertFalse(self.graph.has_operation_parents("s1"))

	def test_has_no_parents(self):
		self.assertTrue(self.graph.has_no_parents("s7"))
		self.assertFalse(self.graph.has_no_parents("s4"))

	def test_operation_nodes(self):
		self.assertItemsEqual(self.graph.operation_nodes(), ["s1", "s2", "s3", "s4", "s5_1", "s5_2", "s6", "s7", "s8"])

	def test_finished_operation_nodes(self):
		self.assertItemsEqual(self.graph.finished_operation_nodes(), ["s5_2", "s6", "s8"])

	def test_resource_nodes(self):
		self.assertItemsEqual(self.graph.resource_nodes(), ["s1-s8", "s4-s7", "s3-s4", "s4-s5", "s6-s5"])

	def test_print_all(self):
		self.graph.print_all()

	def test_edge_connecting_nodes(self):
		print "\n" + str(self.graph.edge_connecting_nodes("s4-s7", "s1")) + "\n"
		print "\n" + str(self.graph.edge_connecting_nodes("s7", "s2")) + "\n"

	def test_edge_weight_on_nodes(self):
		print "\n" + str(self.graph.edge_weight_on_nodes("s4-s7", "s1")) + "\n"
		print "\n" + str(self.graph.edge_weight_on_nodes("s7", "s1")) + "\n"

	def test_critial_path_length_list(self):
		# test CPL calculating and sorting
		cpl_list = critial_path_length_list(self.graph)

		print "\n *** node in its cpl's decreasing order ***"
		for each in cpl_list:
			print "node & its cpl: " + str(each)
		print "*******************************************\n"

		cpl_list = critial_path_length_list(dionysus_dependency_graph())
		self.assertEqual(cpl_list, [])

	def test_schedule_graph(self):
		pass


if __name__ == "__main__":
	unittest.main()








