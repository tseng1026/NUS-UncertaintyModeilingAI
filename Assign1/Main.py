import argparse
import json
import numpy as np
from Tree import Tree, TreeNode
from Inference import sum_product

# Generates a Tree object from data
def build_tree(data: dict) -> Tree:
	num = len(data["nodes"])
	nodes = dict()

	# Create nodes
	for k in range(num):
		nodes[k] = TreeNode(k, data["nodes"][str(k)]["dim"])
	
	tree = Tree(nodes)
	tree.p_0 = np.array(data["p_0"])

	# Create edges
	for f, edge in data["factors"].items():
		for t, factor in edge.items():
			nodes[int(f)].children.append(nodes[int(t)])
			nodes[int(t)].parent = nodes[int(f)]
			tree.factors[f"{f}-{t}"] = np.array(factor)
	return tree

# Test the computed results
def test(tree: Tree, data: dict) -> str:
	marginals = sum_product(tree, data["observations"])
	
	# Check if it is correct
	result = ""
	for k, marginal in marginals.items():
		expected = np.array(data["marginals"][str(k)])
		
		if np.allclose(marginal, expected): result += "T"
	correct = result.count("T")

	print(f"{correct} of {len(result)} marginals correct.")
	return result

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("problems", type = str, nargs = "+", help = "path(s) to problem json files")
	
	args = parser.parse_args()
	for problem in args.problems:
		with open(problem, "r") as file:
			data = json.load(file)
		
		tree = build_tree(data)
		test(tree, data)
