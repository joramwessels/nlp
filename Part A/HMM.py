#! /usr/bin/python

import sys
from posgram import viterbiMatrices as freqs

def main():
	model = HMM(sys.argv[1])
	print(model.getTransitionProbs('NN'))
	print(model.getTagProbs('you'))
	
LE = ["./.", "======================================"]
WE = [' ', '\n']
TD = '/'

class HMM:
	
	def __init__(self, filename):
		print("posgram")
		tr, wt = freqs(filename, 2, line_ends=LE, word_ends=WE, tag_del=TD)
		print("posgram")
		tr1, wt1 = freqs(filename, 1, line_ends=LE, word_ends=WE, tag_del=TD)
		self.transitionProbs = freqsToProbs(tr, tr1)
		self.wordTagProbs = indexTagProbs(wt)
	
	def getTransitionProbs(self, tag):
		dict = self.transitionProbs
		if tag in dict.keys():
			return dict[tag]
		else:
			return {}
	
	def getTagProbs(self, word):
		dict = self.wordTagProbs
		if word in dict.keys():
			return dict[word]
		else:
			return {}

def indexTagProbs(frequencies):
	print("indexTagProbs")
	probs = {}
	for key, value in frequencies.items():
		(word, tag) = key.split(TD)
		if word in probs.keys():
			probs[word][tag] = value
		else:
			probs[word] = {tag : value}
	normalized = {}
	for word, tagProbs in probs.items():
		total = sum(list(tagProbs.values()))
		normalized[word] = {}
		for tag, prob in tagProbs.items():
			normalized[word][tag] = prob / total
	return normalized

def freqsToProbs(biFreqs, uniFreqs):
	print("freqsToProbs")
	gtProbability = turingSmoothing(biFreqs, uniFreqs)
	probs = {}
	for key, value in biFreqs.items():
		(tag1, tag2) = key.split(WE[0])
		if tag1 in probs.keys():
			probs[tag1][tag2] = gtProbability(key)
		else:
			probs[tag1] = {tag2 : gtProbability(key)}
	return probs

def turingSmoothing(Nfreq, N1freq):
	print("turingSmoothing")
	"""Returns a closure that calculates probability using Turing Smoothing.
	
	Args:
		Nfreq (dict): A dictionary mapping N-grams to their frequencies.
		N1freq (dict): A dictionary mapping (N-1)-grams to their frequencies.
	Returns:
		func: A function that calculates the probability of an N-gram.
	
	"""
	Nvalues = list(Nfreq.values())
	N1values = list(N1freq.values())
	print("\tN")
	N = dict([(i, Nvalues.count(i)) for i in Nvalues])
	print("\tN1")
	N1 = dict([(i, N1values.count(i)) for i in N1values])
	def probability(ngram):
		n1gram = ngram.split(' ')[:-1]
		PN = gts(ngram, N, Nfreq)
		PN1 = gts(n1gram, N1, N1freq)
		if PN1 == 0: return 0
		return PN / PN1
	return probability

def gts(ngram, N, Nfreq):
	"""Performs the GTS calculations. 'C' is the frequency of 'ngram',
		Nc is the amount of ngrams with frequency 'C'.
	
	Args:
		ngram (str): The N-gram of which to calculate the prediction.
		N (dict): A dict mapping ngram frequencies to "frequency frequencies".
		Nfreq (dict): A dict mapping N-grams to their frequency.
	Returns:
		float: The GT-smoothed probability of the given N-gram.
	
	"""
	C = frequency(Nfreq, ngram)
	if C == 0:
		return frequency(N, 1) / sum(N.values())
	Nc = frequency(N, C)
	if Nc == 0: print(C, ngram, (ngram in Nfreq))
	Nc1 = frequency(N, C+1)
	return ((C + 1) * Nc1) / Nc

def frequency(freq, elem):
	"""Returns the value of the given key if present, or 0 otherwise.
	
	Args:
		freq (dict): A dictionary.
		elem: Any type of element of which the frequency is requested.
	Returns:
		int: The frequency of the element in the dicionary.
	
	"""
	if elem in list(freq.keys()):
		return freq[elem]
	else:
		return 0

if __name__ == "__main__":
	main()