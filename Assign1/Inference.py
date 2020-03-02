import numpy as np
from functools import reduce
from Tree import Tree, TreeNode
from decimal import *

# Implement the Sum-Product algorithm for directed trees
def sum_product(tree: Tree, observations: dict) -> dict:
	setup_self_factors(tree, observations)
	root = tree.root
	for c in root.children:
			collect(tree, root, c)
	for c in root.children:
			distribute(tree, root, c)
	return compute_marginals(tree)

# Set up self_factors for each node (observed or not)
def setup_self_factors(tree: Tree, observations: dict) -> None:
	# Your code goes here.
	for _, node in tree.nodes.items():
		# initialization
		factor = [1] * node.dim

		# the root node
		if str(node.id) == "0":
			factor = tree.p_0.tolist()[0]
		
		# 1 if the node is not observed
		if str(node.id) not in observations:
			self_factor = factor
		
		# 0 if the node is not observed with exact value
		if str(node.id) in observations:
			self_factor = [0] * node.dim
			self_factor[observations[str(node.id)]] = factor[observations[str(node.id)]]

		# update the final results
		tree.self_factors[node.id] = self_factor


# Collect messages from child node to parent node.
def collect(tree: Tree, to_node: TreeNode, from_node: TreeNode) -> None:
	# Your code goes here.
	for children_node in from_node.children:
		collect(tree, from_node, children_node)
	send_message(tree, from_node, to_node)

# Distribute messages from parent node to child node
def distribute(tree: Tree, from_node: TreeNode, to_node: TreeNode) -> None:
	# Your code goes here.
	send_message(tree, from_node, to_node)
	for children_node in to_node.children:
		distribute(tree, to_node, children_node)

# Send a message from from_node to to_node and store it in tree.messages as cache
def send_message(tree: Tree, from_node: TreeNode, to_node: TreeNode) -> None:
	# Your code goes here.
	messages = [0] * to_node.dim
	for t in range(to_node.dim):
		
		total = 0
		for f in range(from_node.dim):

			# compute for the previous factorization results
			pre = 1
			from_to, from_id, to_id = "", 0, 0
			from_to1 = str(from_node.id) + "-" + str(to_node.id)
			from_to2 = str(to_node.id) + "-" + str(from_node.id)
			if from_to1 in tree.factors: from_to, from_id, to_id = from_to1, f, t
			if from_to2 in tree.factors: from_to, from_id, to_id = from_to2, t, f
			
			self_factor = Decimal(str(tree.self_factors[from_node.id][f]))
			factor      = Decimal(str(tree.factors[from_to][from_id][to_id]))
			pre = self_factor * factor

			# compute for the next factorization results
			nxt = Decimal("1")
			neighbor = [from_node.parent] + from_node.children
			for neighbor_node in neighbor:
				if neighbor_node    == None: continue
				if neighbor_node.id == to_node.id: continue
				nxt *= Decimal(str(tree.messages[(neighbor_node.id, from_node.id)][f]))

			# update the final results
			total += pre * nxt
		messages[t] = float(total)
	
	tree.messages[(from_node.id, to_node.id)] = messages


# Compute the marginals of all nodes in the tree and return them by dict
def compute_marginals(tree: Tree) -> dict:
	# Your code goes here.
	print ("\n[Done] Computing marginal probability!")
	marginals = {}
	for _, node in tree.nodes.items():
		probability = [0] * node.dim
		for k in range(node.dim):
			
			# compute for the previous factorization results
			pre = tree.self_factors[node.id][k]

			# compute for the next factorization results
			nxt = 1
			neighbor = [node.parent] + node.children
			for neighbor_node in neighbor:
				if neighbor_node    == None: continue
				nxt *= tree.messages[(neighbor_node.id, node.id)][k]

			# update the final results
			probability[k] = pre * nxt

		# normalization
		probability = np.array(probability)
		probability = probability / np.sum(probability)
		probability = probability.reshape(1, node.dim)
		marginals[node.id] = probability
		print ("      ", node.id, probability)
	return marginals