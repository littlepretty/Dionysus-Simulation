
from dionysus_dependency_graph import dionysus_dependency_graph
from dionysus_algorithms import *

import pydot
from pygraph.readwrite.dot import write

def update_graph_after_schedule(graph):
	print "*******************************************************"
	print "******** updating graph after last scheduling *********"

	for Oi in graph.finished_operation_nodes():
		# finish add tunnel operation node
		if graph.is_add_tunnel_operation(Oi):
			graph.del_node(Oi)
		# finish delete tunel operation node
		elif graph.is_del_tunnel_operation(Oi):
			if graph.neighbors(Oi):
				Rj = graph.neighbors(Oi)[0]
				l_ij = graph.edge_weight_on_nodes(Oi, Rj)
				free_capacity = graph.free_capacity(Rj) + l_ij
				graph.set_free_capacity(Rj, free_capacity)
			graph.del_node(Oi)
		# finish change weight operation node
		else:
			for Rk in [item for item in graph.neighbors(Oi) if graph.node_type(item) == "resource"]:
				l = graph.edge_weight_on_nodes(Oi, Rk)
				free_capacity = graph.free_capacity(Rk) + l
				graph.set_free_capacity(Rk, free_capacity)
				graph.del_edge( (Oi, Rk) )

			if graph.has_no_parents(Oi):
				graph.del_node(Oi)

	for Ri in graph.resource_nodes():
		sum_l_ij = 0
		for Oj in graph.neighbors(Ri):
			sum_l_ij += graph.edge_weight_on_nodes(Ri, Oj)
		if graph.free_capacity(Ri) >= sum_l_ij:
			new_free_capacity = graph.free_capacity(Ri) - sum_l_ij
			graph.set_free_capacity(Ri, new_free_capacity)
			for child in graph.neighbors(Ri):
				graph.del_edge( (Ri, child) )

	print "******** updating graph end                   *********"
	print "*******************************************************"


def can_schedule_operation(graph, Oi):
	if graph.scheduled(Oi):
		return False
	# add tunnel opeartion node
	if graph.is_add_tunnel_operation(Oi):
		if graph.has_no_parents(Oi):
			return True
		# add tunnel operation node only has 1 parent
		if graph.incidents(finished):
			Rj = graph.incidents(finished)[0]
			l_ji = graph.edge_weight_on_nodes(Rj, Oi)
			if graph.free_capacity(Rj) >= l:
				free_capacity = graph.free_capacity(Rj) - l_ji
				graph.set_free_capacity(Rj, free_capacity)
				graph.del_edge((Rj, Oi))
				return True
			return False
	# delete tunnel operation node
	elif graph.is_del_tunnel_operation(Oi):
		if graph.has_no_parents(Oi):
			return True
		return False

	# change weight operation node
	else:
		if graph.has_no_parents(Oi):
			can_schedule = True
		else:
			can_schedule = False

		total = 0
		available = 0
		if graph.has_operation_parents(Oi):
			available = 0
		else:
			# obtain possible free capacity as resource
			for Rk in [item for item in graph.incidents(Oi) if graph.node_type(item) == "resource"]:
				free_capacity = graph.free_capacity(Rk)
				available = min( [available, free_capacity] )
			# update edge weight on (resource_node, this_node)
			for Rk in [item for item in graph.incidents(Oi) if graph.node_type(item) == "resource"]:
				l_ki = graph.edge_weight_on_nodes(Rk, Oi) - available
				graph.set_edge_weight((Rk, Oi), l_ki)
				free_capacity = graph.free_capacity(Rk) - available
				graph.set_free_capacity(Rk, free_capacity)

		total += available
		# if there is any available resource
		if total > 0:
			can_schedule = True

		return can_schedule

def schedule_graph_without_path_node(graph):
	
	scheduled_order = []
	scheduled_nodes = []

	num_operation_nodes = len(graph.operation_nodes())

	step = 0
	num_scheduled_nodes = 0

	while num_scheduled_nodes != num_operation_nodes:

		update_graph_after_schedule(graph)

		dot = write(graph)
		graph_dot = pydot.graph_from_dot_data(dot)
		graph_dot.write_png("FR_case_without_path_node_step_%d.png" % step)
		step += 1

		cpl_list = critial_path_length_list(graph)

		print "*** node in cpl's decreasing order ***"
		for each in cpl_list:
			print "node & its cpl: " + str(each)

		for each in cpl_list:
			(node, cpl) = each
			if can_schedule_operation(graph, node):
				scheduled_nodes.append(node)
				num_scheduled_nodes += 1
				print "*** scheduled nodes: " + str(scheduled_nodes)
				
		for each in scheduled_nodes:
			graph.set_scheduled(each)
		scheduled_order.append(scheduled_nodes)
		scheduled_nodes = []
		
	return scheduled_order

	



