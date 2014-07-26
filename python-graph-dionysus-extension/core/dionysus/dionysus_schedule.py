
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
	






































