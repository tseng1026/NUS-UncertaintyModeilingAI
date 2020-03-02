class TreeNode:
	def __init__(self, node_id, dim, parent=None):
		self.id  = node_id
		self.dim = dim

		self.parent   = parent
		self.children = []

	def __str__(self):
		return f'(id={self.id}, dim={self.dim})'
	def __repr__(self):
		return f'(id={self.id}, dim={self.dim})'

class Tree:
	def __init__(self, nodes):   
		self.p_0   = None			# prior probability of root node (Numpy array)
		self.root  = nodes[0]		# root node			(TreeNode)
		self.nodes = nodes			# all nodes			(dict = { node_id  : TreeNode})

		self.messages = {}			# cache messages	(dict = {(from, to): message})
		self.factors  = {}			# factors CPT		(dict = {"from-to" : probability})
		self.self_factors = {}		# factors observe	(dict = { node_id  : probability})