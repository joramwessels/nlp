#! /usr/bin/python
"""
NLP Part B
Amir Alnomani		10437797
Maurits Offerhaus	10400036
Joram Wessels		10631542
"""
hValue = 2
vValue = 2

def binarizeTreebank(treebank, h, v):
	"""Sets the global 'hValue' and 'vValue' variables and binarizes all trees.
	
	Args:
		treebank (list): A list of non-binarized treebanks.
		h (int): The order of horizontal Markovization.
		v (int): The order of vertical Markovization.
	Returns:
		list: A list of binarized treebanks.
	
	"""
	global hValue, vValue
	hValue, vValue = h, v
	return [binarize(tree) for tree in treebank]

def binarize(sent, v=['']*vValue, h=['']*hValue):
	"""Binarizes a sentence using both vertical- and horizontal Markovization of
		the orders specified by the 'vValue' and 'hValue' variables respectively.
	
	Args:
		sent (list): The sentence to be binarized, represented as a list of lists.
		v (list): (optional) The vertical Markovization queue that keeps track
			of the parent node POS tags. It is only used in recursive steps.
		h (list): (optional) The horizontal Markovization queue that keeps track
			of the sibling node POS tags. It is only used in recursive steps.
	Returns:
		list: The binarized sentence, represented as a list of lists.
	
	"""
	# terminal symbols are the basecase
	if isTerminal(sent): return sent
	# add the new POS tags to the vertical- and horizontal Markovization queues
	vert = [sent[0]] + v[:-1]
	hori  = h[1:] + [sent[1][0]]
	# determine the POS tag of the right node using Markovization
	rightLabel = '@' + joinLabels('^', vert) + "->_" + joinLabels('_', hori)
	# clearing the horizontal Markovization queue prior to binarizing the left node
	leftNode = binarize(sent[1], v=vert)
	# upon encountering a unary node, clear the horizontal Markovization queue and binarize the first element
	if len(sent) == 2: return [joinLabels('^', vert), binarize(sent[1], v=vert)]
	# upon encountering a binary node, binarize the right node using the horizontal Markovization queue
	elif len(sent) == 3: rightNode = [rightLabel, binarize(sent[2], v=vert)]
	# upon encountering more than 2 nodes, binarize every node after index 1 using the same
	# Markovization state as the current node and append the content to the new POS tag
	elif len(sent) > 3: rightNode = [rightLabel] + binarize([sent[0]] + sent[2:], v=v, h=hori)[1:]
	# return the vertically Markovized POS tag along with its two nodes
	return [joinLabels('^', vert), leftNode, rightNode]

def joinLabels(sep, list):
	"""Joins a list, excluding empty strings.
	"""
	return sep.join([x for x in list if x != ''])

def isTerminal(sent):
	"""Checks if a (sub-)sentence is a terminal symbol.
	"""
	if any([not (isinstance(x, str) or isinstance(x, list)) for x in sent]):
		raise TypeError("Incompatible data type encountered.")
	elif len(sent) == 2:
		if isinstance(sent[0], str) and isinstance(sent[1], str): return True
		return False
	elif len(sent) > 2:
		return False
	else:
		raise Exception("Sentence of length '%d' encountered: '%s'" %(len(sent), sent))

def printTree(sent, depth):
	"""Prints a sentence as an indented tree.
	"""
	for i in range(depth): print(' ', end='')
	if isinstance(sent, str):
		print(sent)
	else:
		print(sent[0])
		for x in sent[1:]: printTree(x, depth + 1)