
from pygraph.classes.exceptions import AdditionError
from pygraph.classes.digraph import digraph

class dionysus_dependency_graph(digraph):
	"""dependency graph for dionysus simulation"""

	DIRECTED = True

	def __init__(self):
		digraph.__init__(self)

	def add_operation_node(self, node, operation_type, weight = 1, scheduled = False):
		self.add_node(node, [ ("attrs", {"type": "operation", "weight": weight, "scheduled": scheduled, "operation_type": operation_type} ) ])

	def add_resource_node(self, node, free_capacity = 0, weight = 0):
		self.add_node(node, [ ("attrs",  {"type": "resource", "weight": weight, "free_capacity": free_capacity} ) ])

	def add_path_node(self, node, committed = 0, weight = 0, ):
		self.add_node(node, [ ("attrs",  {"type": "path", "weight": weight, "committed": committed} ) ])

	def node_type(self, node):
		"""
		@type  node: node
		@param node: node identifier

		@rtype:  string
		@return: A string indicate node's type
			1. operation node
			2. resource node
			3. path node
		"""
		(attrs, vals) = self.node_attributes(node)[0]
		if "type" in vals:
			return vals["type"]
		else:
			raise AdditionError( "type is missing in %s" % node )

	def node_weight(self, node):
		(attrs, vals) = self.node_attributes(node)[0]
		if "weight" in vals:
			return vals["weight"]
		else:
			raise AdditionError( "weight is missing in %s" % node )

	def scheduled(self, node):
		(attrs, vals) = self.node_attributes(node)[0]

		if self.node_type(node) == "operation":
			if "scheduled" in vals:
				return vals["scheduled"]
			else:
				raise AdditionError( "scheduled is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a operation node" % node )

	def free_capacity(self, node):
		(attrs, vals) = self.node_attributes(node)[0]

		if self.node_type(node) == "resource":
			if "free_capacity" in vals:
				return vals["free_capacity"]
			else:
				raise AdditionError( "free_capacity is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a resource node" % node )

	def committed(self, node):
		(attrs, vals) = self.node_attributes(node)[0]

		if self.node_type(node) == "path":
			if "committed" in vals:
				return vals["committed"]
			else:
				raise AdditionError( "committed is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a path node" % node )

	def set_scheduled(self, node, scheduled = True):
		(attrs, vals) = self.node_attributes(node)[0]

		if self.node_type(node) == "operation":
			if "scheduled" in vals:
				vals["scheduled"] = scheduled
			else:
				raise AdditionError( "scheduled is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a operation node" % node )

	def set_free_capacity(self, node, free_capacity):
		(attrs, vals) = self.node_attributes(node)[0]

		if self.node_type(node) == "resource":
			if "free_capacity" in vals:
				vals["free_capacity"] = free_capacity
			else:
				raise AdditionError( "free_capacity is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a resource node" % node )

	def set_committed(self, node, committed):
		(attrs, vals) = self.node_attributes(node)[0]

		if self.node_type(node) == "path":
			if "committed" in vals:
				vals["committed"] = committed
			else:
				raise AdditionError( "committed is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a path node" % node )

	def print_nodes(self):
		for each in self.nodes():
			print "node " + str(each) + " attributes: " + str(self.node_attributes(each)[0][1])

			# if self.node_type(each) == "resource":
			# 	print "free capacity: " + str(self.free_capacity(each))
			# elif self.node_type(each) == "path":
			# 	print "path committed: " + str(self.committed(each))
			# elif self.node_type(each) == "operation":
			# 	print "scheduled: " + str(self.scheduled(each))

	def print_edges(self):
		for each in self.edges():
			print "edge: " + str(each) + " weight: " + str(self.edge_weight(each))

	def print_all(self):
		print "\n************************ nodes **************************"
		self.print_nodes()
		print "\n************************ edges **************************"
		self.print_edges()

	def print_nodes_with_attributes(self):
		# test operation_nodes()
		print "*** all nodes with attributs ***"
		for each in self.operation_nodes():
			print "node " + str(each) + " attributes: " + str(self.node_attributes(each)[0][1])
		# test finished_operation_nodes()
		for each in self.finished_operation_nodes():
			print "node " + str(each) + " attributes: " + str(self.node_attributes(each)[0][1])
		# test resource_nodes()
		for each in self.resource_nodes():
			print "node " + str(each) + " attributes: " + str(self.node_attributes(each)[0][1])

		print "*********************************"


	def is_add_tunnel_operation(self, node):
		(attrs, vals) = self.node_attributes(node)[0]
		if self.node_type(node) == "operation":
			if "operation_type" in vals:
				return vals["operation_type"] == "add_tunnel"
			else:
				raise AdditionError( "operation_type is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a operation node" % node )

	def is_del_tunnel_operation(self, node):
		(attrs, vals) = self.node_attributes(node)[0]
		if self.node_type(node) == "operation":
			if "operation_type" in vals:
				return vals["operation_type"] == "del_tunnel"
			else:
				raise AdditionError( "operation_type is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a operation node" % node )

	def is_chg_weight_operation(self, node):
		(attrs, vals) = self.node_attributes(node)[0]
		if self.node_type(node) == "operation":
			if "operation_type" in vals:
				return vals["operation_type"] == "chg_weight"
			else:
				raise AdditionError( "operation_type is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a operation node" % node )


	def has_operation_parents(self, node):
		parenets = self.incidents(node)
		for each in parenets:
			if self.node_type(each) == "operation":
				return True
		return False

	def has_no_parents(self, node):
		parenets = self.incidents(node)
		return len(parenets) == 0

	def operation_nodes(self):
		return [item for item in self.nodes() if self.node_type(item) == "operation"]

	def finished_operation_nodes(self):
		operation_node_list = self.operation_nodes()
		return [item for item in operation_node_list if self.scheduled(item) == True]

	def resource_nodes(self):
		return [item for item in self.nodes() if self.node_type(item) == "resource"]

	def path_nodes(self):
		return [item for item in self.nodes() if self.node_type(item) == "path"]

	def edge_connecting_nodes(self, start, end):
		edges = [item for item in self.edges() if item[0] == start and item[1] == end]
		if edges:
			return edges[0]
		else:
			return []

	def edge_weight_on_nodes(self, start, end):
		edge = self.edge_connecting_nodes(start, end)
		if edge:
			return self.edge_weight(edge)
		else:
			return -999999999




