
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
			""" a little tweet: if Oi have no path parents, but have resource parents """
			path_parents = [item for item in graph.incidents(Oi) if graph.node_type(item) == "path"]
			if len(path_parents):
				for Pj in [item for item in graph.neighbors(Oi) if graph.node_type(item) == "path"]:
					for Rk in [item for item in graph.neighbors(Pj) if graph.node_type(item) == "resource"]:
						l_jk = graph.edge_weight_on_nodes(Pj, Rk)
						l_jk -= graph.committed(Pj)
						free_capacity = graph.free_capacity(Rk) + graph.committed(Pj)
						graph.set_free_capacity(Rk, free_capacity)
						if l_jk == 0:
							graph.del_edge( (Pj, Rk) )
					graph.set_committed(Pj, 0)
					if graph.edge_weight_on_nodes(Oi, Pj) == 0:
						graph.del_node(Pj)

				for Pj in [item for item in graph.incidents(Oi) if graph.node_type(item) == "path"]:
					if graph.edge_weight_on_nodes(Pj, Oi) == 0:
						graph.del_node(Pj)
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
			free_capacity = graph.free_capacity(Ri) - sum_l_ij
			graph.set_free_capacity(Ri, free_capacity)
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
		if graph.incidents(Oi):
			Rj = graph.incidents(Oi)[0]
			l_ji = graph.edge_weight_on_nodes(Rj, Oi)
			if graph.free_capacity(Rj) >= l_ji:
				free_capacity = graph.free_capacity(Rj) - l_ji
				graph.set_free_capacity(Rj, free_capacity)
				graph.del_edge((Rj, Oi))
				return True
			return False
	# delete tunnel operation node
	if graph.is_del_tunnel_operation(Oi):
		if graph.has_no_parents(Oi):
			return True
		return False

	# change weight operation node
	total = 0
	
	if graph.has_no_parents(Oi):
		can_schedule = True
	else:
		can_schedule = False

	""" a little tweet: if Oi have no path parents, but have resource parents """
	path_parents = [item for item in graph.incidents(Oi) if graph.node_type(item) == "path"]
	if len(path_parents):

		for Pj in path_parents:
			
			available = graph.edge_weight_on_nodes(Pj, Oi)
			
			if graph.has_operation_parents(Pj):
				available = 0
			else:
				resource_parents = [item for item in graph.incidents(Oi) if graph.node_type(item) == "resource"]
				for Rk in resource_parents:
					l_kj = graph.edge_weight_on_nodes(Rk, Pj)
					free_capacity = graph.free_capacity(Rk)
					available = min( [available, l_kj, free_capacity] )
				for Rk in resource_parents:
					l_kj = graph.edge_weight_on_nodes(Rk, Pj) - available
					graph.set_edge_weight((Rk, Pj), l_kj)
					free_capacity = graph.free_capacity(Rk) - available
					graph.set_free_capacity(Rk, free_capacity)
			total += available
			l_ji = graph.edge_weight_on_nodes(Pj, Oi) - available
			graph.set_edge_weight((Pj, Oi), l_ji)

	else:
		available = 0
		if graph.has_operation_parents(Oi):
			available = 0
		else:
			resource_parents = [item for item in graph.incidents(Oi) if graph.node_type(item) == "resource"]

			# obtain possible free capacity as resource
			for Rk in resource_parents:
				free_capacity = graph.free_capacity(Rk)
				available = min( [available, free_capacity] )
			# update edge weight on (resource_node, this_node)
			for Rk in resource_parents:
				l_ki = graph.edge_weight_on_nodes(Rk, Oi) - available
				graph.set_edge_weight((Rk, Oi), l_ki)
				free_capacity = graph.free_capacity(Rk) - available
				graph.set_free_capacity(Rk, free_capacity)
		total += available

	if total > 0:
		can_schedule = True

	path_children = [item for item in graph.neighbors(Oi) if graph.node_type(item) == "path"]
	for Pj in path_children:
		l_ij = graph.edge_weight_on_nodes(Oi, Pj)
		committed = graph.committed(Pj)
		graph.set_committed(Pj, min( [l_ij, total] ))
		l_ij -= graph.committed(Pj)
		graph.set_edge_weight((Oi, Pj), l_ij)
		total -= graph.committed(Pj)

	return can_schedule

def schedule_graph(graph):
	
	scheduled_order = []
	scheduled_nodes = []

	num_operation_nodes = len(graph.operation_nodes())

	step = 0
	num_scheduled_nodes = 0

	while num_scheduled_nodes != num_operation_nodes:

		update_graph_after_schedule(graph)

		dot = write(graph)
		graph_dot = pydot.graph_from_dot_data(dot)
		graph_dot.write_png("FR_case_step_%d.png" % step)
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






















































