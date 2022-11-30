#!/usr/bin/env python3

def dissect(depth_lst, value_lst) :
	print(depth_lst)
	print(value_lst)
	value_lst = list(value_lst)
	for d, n in enumerate(depth_lst) :
		for e in range(n) :
			yield d, value_lst.pop(0)
			
def push(depth, value, tree, level=0) :
	#print("{0}push({1}, {2}, {3}, {4})".format('\t'*level, depth, value, tree, level))
	if not isinstance(tree, list) :
		return False
	if depth == level :
		if tree[0] is None :
			tree[0] = value
		elif tree[1] is None :
			tree[1] = value
		else :
			return False
		return True
	else :
		if tree[0] is None :
			tree[0] = [None, None]
		if push(depth, value, tree[0], level+1) :
			return True
		if tree[1] is None :
			tree[1] = [None, None]
		if push(depth, value, tree[1], level+1) :
			return True
		return False
		
def unfold(tree, result=None, path='') :
	if result is None :
		result = dict()
	for n, node in enumerate(tree) :
		p = path + str(n)
		if isinstance(node, list) :
			unfold(node, result, p)
		elif node is not None :
			result[node] = p
	return result

class HuffmanTable() :
	def __init__(self, depth_lst, value_lst) :
		self.tree = [None, None]
		for depth, value in dissect(depth_lst, value_lst) :
			self.insert(depth, value)
		
	def insert(self, depth, value) :
		push(depth, value, self.tree)
		
	def get(self, pth) :
		node = self.tree
		while not isinstance(node, bytes) :
			print(node)
			s = pth.pop(0)
			node = node[s]
		return node
		
	def expand(self, s) :
		node = self.tree
		for c in s :
			for i in "{0:b}".format(c) :
				node = node[int(i)]
				if node is None :
					raise ValueError
				elif isinstance(node, int) :
					yield node
					node = self.tree
		s = bytearray(s)
		
	def compress(self, s) :
		u = unfold(self.tree)
		
			
if __name__ == '__main__' :
	
	depth_lst = [0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
	value_lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
	
	ref_tree = [[0, [1, 2]], [[3, 4], [5, [6, [7, [8, [9, [10, [11, None]]]]]]]]]
	tst = HuffmanTable(depth_lst, value_lst)
	
	print(tst.tree)
	
	assert(tst.tree == ref_tree)
	
	print(unfold(tst.tree))
	
