
from pygraph.classes.exceptions import AdditionError
from pygraph.classes.digraph import digraph

class dionysus_dependency_graph(digraph):
	"""dependency graph for dionysus simulation"""

	DIRECTED = True

	def __init__(self):
		digraph.__init__(self)

	def add_operation_node(self, node, weight = 1, scheduled = False):
		self.add_node(node, [("type", "operation"), ("weight", weight), ("scheduled", scheduled)])

	def add_resource_node(self, node, weight = 0, free_capacity = 0):
		self.add_node(node, [("type", "resource"), ("weight", weight), ("free_capacity", free_capacity)])

	def add_path_node(self, node, weight = 0, committed = 0):
		self.add_node(node, [("type", "path"), ("weight", weight), ("committed", committed)])

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
		attrs = self.node_attributes(node)
		(key, val) = attrs[0]
		if key == "type":
			return val
		else:
			raise AdditionError( "type is missing in %s" % node )

	def node_weight(self, node):
		attrs = self.node_attributes(node)
		(key, val) = attrs[1]
		if key == "weight":
			return val
		else:
			raise AdditionError( "weight is missing in %s" % node )

	def scheduled(self, node):
		attrs = self.node_attributes(node)

		if self.node_type(node) == "operation":
			(key, val) = attrs[2]
			if key == "scheduled":
				return val
			else:
				raise AdditionError( "scheduled is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a operation node" % node )

	def free_capacity(self, node):
		attrs = self.node_attributes(node)

		if self.node_type(node) == "resource":
			(key, val) = attrs[2]
			if key == "free_capacity":
				return val
			else:
				raise AdditionError( "free_capacity is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a resource node" % node )

	def committed(self, node):
		attrs = self.node_attributes(node)
		if self.node_type(node) == "path":
			(key, val) = attrs[2]
			if key == "committed":
				return val
			else:
				raise AdditionError( "committed is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a path node" % node )

	def set_scheduled(self, node, scheduled = True):
		attrs = self.node_attributes(node)

		if self.node_type(node) == "operation":
			(key, val) = attrs[2]
			if key == "scheduled":
				attrs[2] = (key, scheduled)
			else:
				raise AdditionError( "scheduled is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a operation node" % node )

	def set_free_capacity(self, node, free_capacity = 0):
		attrs = self.node_attributes(node)

		if self.node_type(node) == "resource":
			(key, val) = attrs[2]
			if key == "free_capacity":
				attrs[2] = (key, free_capacity)
			else:
				raise AdditionError( "free_capacity is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a resource node" % node )

	def set_committed(self, node, committed = 0):
		attrs = self.node_attributes(node)
		if self.node_type(node) == "path":
			(key, val) = attrs[2]
			if key == "committed":
				attrs[2] = (key, committed)
			else:
				raise AdditionError( "committed is missing in %s" % node )
		else:
			raise AdditionError( "%s is not a path node" % node )

	def print_nodes(self):
		for each in self.nodes():
			print "node " + str(each) + " weight: " + str(self.node_weight(each))

			if self.node_type(each) == "resource":
				print "free capacity: " + str(self.free_capacity(each))
			elif self.node_type(each) == "path":
				print "path committed: " + str(self.committed(each))
			elif self.node_type(each) == "operation":
				print "scheduled: " + str(self.scheduled(each))

	def print_edges(self):
		for each in self.edges():
			print "edge: " + str(each) + " weight: " + str(self.edge_weight(each))

	def print_all(self):
		self.print_nodes()
		self.print_edges()





