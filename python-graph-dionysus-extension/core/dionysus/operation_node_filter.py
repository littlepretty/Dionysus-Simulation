
class operation_node_filter(object):
    """
    if node is operation_node filter.
    """
    
    def __init__(self):
        """
        Initialize the filter.
        """
        self.graph = None
        self.spanning_tree = None
    
    def configure(self, graph, spanning_tree):
        """
        Configure the filter.
        
        @type  graph: graph
        @param graph: Graph.
        
        @type  spanning_tree: dictionary
        @param spanning_tree: Spanning tree.
        """
        self.graph = graph
        self.spanning_tree = spanning_tree
         
    def __call__(self, node, parent):
        """
        Decide if the given node should be included in the search process.
        
        @type  node: node
        @param node: Given node.
        
        @type  parent: node
        @param parent: Given node's parent in the spanning tree.
        
        @rtype: boolean
        @return: Whether the given node should be included in the search process. 
        """
        if self.graph.node_type(node) == "operation":
            return True
        else:
            return False






            