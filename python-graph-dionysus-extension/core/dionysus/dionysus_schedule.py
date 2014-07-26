
from dionysus_dependency_graph import dionysus_dependency_graph
from dionysus_algorithms import *

def update_graph_after_schedule(graph):
	for finished in graph.finished_operation_nodes():
		# finish add tunnel operation node
		if graph.is_add_tunnel_operation(finished):
			graph.del_node(finished)
		# finish delete tunel operation node
		elif graph.is_del_tunnel_operation(finished):
			if graph.neighbors(finished):
				child = graph.neighbors(finished)[0]
				l = graph.edge_weight_on_nodes(finished, child)
				free_capacity = graph.free_capacity(child) + l
				graph.set_free_capacity(child, free_capacity)
				graph.del_node(finished)
		# finish change weight operation node
		else:
			for path_node in [item for item in graph.neighbors(finished) if graph.node_type(item) == "path"]:
				for resource_node in [item for item in graph.neighbors(path_node) if graph.node_type(item) == "resource"]:
					l = graph.edge_weight_on_nodes(path_node, resource_node)
					l -= graph.committed(path_node)
					free_capacity = graph.free_capacity(resource_node) + graph.committed(path_node)
					graph.set_free_capacity(resource_node, free_capacity)
					if l == 0:
						graph.del_edge( (path_node, resource_node) )
				graph.set_committed(path_node, 0)
				if graph.edge_weight_on_nodes(finished, path_node) == 0:
					graph.del_node(path_node)

			for path_node in [item for item in graph.incidents(finished) if graph.node_type(item) == "path"]:
				if graph.edge_weight_on_nodes(path_node, finished) == 0:
					graph.del_node(path_node)

			if graph.has_no_parents(finished):
				graph.del_node(finished)


	for resource_node in graph.resource_nodes():
		sum_lij = 0
		for child in graph.neighbors(resource_node):
			sum_lij += graph.edge_weight_on_nodes(resource_node, child)
		if graph.free_capacity(resource_node) >= sum_lij:
			new_free_capacity = graph.free_capacity(resource_node) - sum_lij
			graph.set_free_capacity(resource_node, new_free_capacity)
			for child in graph.neighbors(resource_node):
				graph.del_edge( (resource_node, child) )


def can_schedule_operation(graph, node):
	# add tunnel opeartion node
	if graph.is_add_tunnel_operation(node):
		if graph.has_no_parents(node):
			return True
		# add tunnel operation node only has 1 parent
		if graph.incidents(finished):
			parent = graph.incidents(finished)[0]
			l = graph.edge_weight_on_nodes(parent, node)
			if graph.free_capacity(parent) >= l:
				free_capacity = graph.free_capacity(parent) - l
				graph.set_free_capacity(parent, free_capacity)
				graph.del_edge((parent, node))
				return True
			return False
	# delete tunnel operation node
	if graph.is_del_tunnel_operation(node):
		if graph.has_no_parents(node):
			return True
		return False
	# change weight operation node
	total = 0
	can_schedule = False

	for path_node in [item for item in graph.incidents(node) if graph.node_type(item) == "path"]:
		available = graph.edge_weight_on_nodes(path_node, node)
		
		if graph.has_no_parents(path_node):
			available = 0
		else:
			for resource_node in [item for item in graph.incidents(path_node) if graph.node_type(item) == "resource"]:
				l = graph.edge_weight_on_nodes(resource_node, path_node)
				free_capacity = graph.free_capacity(resource_node)
				available = min( [available, l, free_capacity] )
			for resource_node in [item for item in graph.incidents(path_node) if graph.node_type(item) == "resource"]:
				l = graph.edge_weight_on_nodes(resource_node, path_node) - available
				graph.set_edge_weight((resource_node, path_node), l)
				free_capacity = graph.free_capacity(resource_node) - available
				graph.set_free_capacity(resource_node, free_capacity)

		total += available
		l = graph.edge_weight_on_nodes(path_node, node) - available
		graph.set_edge_weight((path_node, node), l)

	if total > 0:
		can_schedule = True

	for path_node in [item for itme in graph.neighbors(node) if graph.node_type(item) == "path"]:
		l = graph.edge_weight_on_nodes(node, path_node)
		committed = graph.committed(path_node)
		graph.set_committed(path_node, min( [l, total] ))
		l -= graph.committed(path_node)
		graph.set_edge_weight((node, path_node), l)
		total -= graph.committed(path_node)

	return can_schedule

















































