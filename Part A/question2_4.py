#! /usr/bin/python

def probabilities(sentenceProbs, filename):
	setA = ["know","I","opinion","do","be","your","not","may","what"]
	setB = ["I","do","not","know"]
	PermsOfA = list(itertools.permutations(setA))
	PermsOfB = list(itertools.permutations(setB))
	
	for permA,PermB in zip(PermsOfA,PermsOfB):
		permA = " ".join(permA)
		permB = " ".join(permB)
	return {}