#! /usr/bin/python

from posgram import viterbiMatrices as freqs

class HMM:
	
	LE = ["./.", "======================================"]
	WE = [' ', '\n']
	TD = '/'
	
	def __init__(self, filename):
		tr, wt = freqs(filename, 2, line_ends=LE, word_ends=WE, tag_del=TD)
		self.transitionProbs = freqsToProbs(tr)
		self.wordTagProbs = indexTagProbs(wt)
	
	def getTransitionProb(self, Tag1, Tag2):
		dict = self.transitionProbs
		gram = (Tag1 + WE[0] + Tag2)
		if gram in dict.keys():
			freq = dict[gram]
		else:
			freq = 0
	
	def getTagProbs(self, word):
		dict = self.wordTagProbs
		if word in dict.keys():
			return dict[word]
		else:
			return {}

def indexTagProbs(frequencies):
	probs = {}
	for key, value in frequencies.items():
		(word, tag) = key.split(TD)
		if word in probs.keys():
			probs[word][tag] = value
		else:
			probs[word] = {tag : value}
	normalized = {}
	for word, tagProbs in probs.items():
		total = sum([val for val in tagProbs.values()])
		normalized[word] = {}
		for tag, prob in tagProbs.items():
			normalized[word][tag] = prob / total
	return normalized

def freqsToProbs(frequencies):
	probs = {}
	for key, value in frequencies.items():
		# TODO calculate probability
		probability = 0
		probs[key] = probability
	return probs