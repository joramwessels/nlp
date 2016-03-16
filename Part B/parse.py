
sentence = ['S', ['NP', ['DT', 'A'], ['NN', 'record'], ['NN','date']]]
sentence2 = ['NP', ['NNP', 'Rolls Royce'], ['NNP', 'motor'], ['NNPS','cars'],['NNP','Inc']]
sentence3 = ['NP', ['DT', 'A'], ['NN', 'record'], ['NN','date'],['NP', ['NNP', 'Rolls Royce'], ['NNP', 'motor'], ['NNPS','cars'],['NNP','Inc']]]
sentence4 = ['ROOT', ['S', ['NP', ['NNP', 'Ms.'], ['NNP', 'Haag']], ['VP', ['VBZ', 'plays'], ['NP', ['NNP', 'Elianti']]], ['.', '.']]]

hValue = 2
vValue = 2

def binarize(sent, v, h):
	"""
	[POS word] -> [POS word]
	[POS2 Non-Terminal] -> [POS2^POS1 binarize(Non-Terminal)]
	[POS2 NT1 NT2] -> [POS2^POS1 binarize(NT1) [@POS2^POS1->_NT1 binarize(NT2)]]
	[POS2 NT1 NT2 NT3] -> [POS2^POS1 NT1 [POS3^POS2 NT2 NT3]]
	"""
	if isTerminal(sent): return sent
	print(sent)
	predicates = [sent[0]] + v[:-1]
	variables  = h[1:] + [sent[1][0]]
	rightLabel = '@' + joinLabels('^', predicates) + "->_" + joinLabels('_', variables)
	leftNode = binarize(sent[1], predicates, ['']*hValue)
	if len(sent) == 2: return [joinLabels('^', predicates), binarize(sent[1], predicates, ['']*hValue)]
	elif len(sent) == 3: rightNode = [rightLabel, binarize(sent[2], predicates, variables)]
	elif len(sent) > 3: rightNode = [rightLabel, binarize([sent[0]] + sent[2:], v, variables)]
	return [joinLabels('^', predicates), leftNode, rightNode]

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

print(binarize(sentence4, ['']*vValue, ['']*hValue))
printTree(binarize(sentence4, ['']*vValue, ['']*hValue), 0)