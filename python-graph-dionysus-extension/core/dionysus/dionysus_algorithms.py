
from dionysus_dependency_graph import dionysus_dependency_graph
from operation_node_filter import operation_node_filter
from pygraph.algorithms.searching import depth_first_search

def critial_path_length_list(graph):

	def recursive_critical_path_length(node):
		# check if recursive function has calculated once		
		have = [item for item in cpl_tuples if node in item]
		if have:
			exsisted = have[0]
			return exsisted[1]

		# find max cpl in node's children
		neighbors = graph.neighbors(node)
		if not neighbors:
			# bottom of recursive call
			if graph.node_type(node) == "operation":
				cpl_tuples.append((node, 1))
				return 1
			else:
				cpl_tuples.append((node, 0))
				return 0

		else:
			children_cpls = []
			# recursively calculate every child's cpl
			for each in neighbors:
				chl_cpl = recursive_critical_path_length(each)
				children_cpls.append(chl_cpl)
			# find max on 
			max_chl_cpl = max(children_cpls)
			# add 1 or 0 based on node's type
			if graph.node_type(node) == "operation":
				cpl = max_chl_cpl + 1
			else:
				cpl = max_chl_cpl + 0
			cpl_tuples.append((node, cpl))
			return cpl 


	(spanning_tree, pre_order, post_order) = depth_first_search(graph, None, operation_node_filter())
	
	# iter_order = topology_order.reverse = post_order
	iter_order = post_order
	print "*** node in topology's reverse order ***"
	for each in iter_order:
		print "node: " + str(each)

	cpl_tuples = []

	for each in iter_order:
		recursive_critical_path_length(each)

	# sort node by its cpl in decreasing order
	sorted_cpl_list = sorted(cpl_tuples, key = lambda cpl_tuple: cpl_tuple[1], reverse = True)
	# only keep operation nodes
	sorted_operation_cpl_list = [item for item in sorted_cpl_list if graph.node_type(item[0]) == "operation"]
	
	return sorted_operation_cpl_list










