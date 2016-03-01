#! /usr/bin/python

import sys
from posgram import countPOSFreqs as POSFreqs

def main():
	model = HMM(sys.argv[1])
	print(model.getTagVocab())
	print(model.getWordVocab()[:10])
	print(model.getTransitionProbs()[:5])
	print(model.getTagProbs()[:5])
	
LE = ["./.", "======================================"]
WE = [' ', '\n']
TD = '/'

class HMM:
	
	def __init__(self, filename):
		tr, wt = POSFreqs(filename, 2, line_ends=LE, word_ends=WE, tag_del=TD)
		tr1, _ = POSFreqs(filename, 1, line_ends=LE, word_ends=WE, tag_del=TD)
		self.tagVocab = getTagVocab(wt)
		self.transitionProbs = freqsToProbs(tr, tr1, self.tagVocab)
		self.wordTagProbs, self.wordVocab = indexTagProbs(wt, self.tagVocab)
	
	def getTagVocab(self):
		return self.tagVocab
	
	def getWordVocab(self):
		return self.wordVocab
	
	def getTransitionProbs(self):
		return self.transitionProbs
	
	def getTagProbs(self):
		return self.wordTagProbs

def getTagVocab(frequencies):
	"""Extracts the vocabulary of tags from a dict of word-tag frequencies.
	
	Args:
		frequencies (dict): A dictionary mapping word-tags to their frequency.
	Returns:
		list: The ordered vocabulary of all possible tags.
	
	"""
	tagVocab = []
	for key in frequencies.keys():
		tag = key.split(TD)[1]
		if not tag in tagVocab:
			tagVocab.append(tag)
	return tagVocab

def indexTagProbs(frequencies, tagVocab):
	print("in HMM.py:indexTagProbs")
	"""Converts word-tag frequencies into a Viterbi matrix.
	
	Args:
		frequencies (dict): A dictionary mapping word-tags to their frequency.
		tagVocab (list): The vocabulary of possible tags.
	Returns:
		list, list: The Vitarbi matrix of word-tag probabilities, as well as
					the ordered vocabulary of all words in the corpus.
	
	"""
	probs = {}
	for key, value in frequencies.items():
		(word, tag) = key.split(TD)
		tagIndex = tagVocab.index(tag)
		if word in probs.keys():
			probs[word][tagIndex] = value
		else:
			probs[word] = [0]*len(tagVocab)
			probs[word][tagIndex] = value
	normalized = []
	wordVocab = []
	for word, tagProbs in probs.items():
		total = sum(tagProbs)
		wordVocab.append(word)
		normalized.append([freq / total for freq in tagProbs])
	return normalized, wordVocab

def freqsToProbs(biFreqs, uniFreqs, tagVocab):
	print("in HMM.py:freqsToProbs")
	"""Converts the bigram- and unigram frequencies to a Viterbi matrix.
	
	Args:
		biFreqs (dict): A dictionary mapping tag bigrams to their frequency.
		uniFreqs (dict): A dictionary mapping tag unigrams to their frequency.
		tagVocab (list): The vocabulary of possible tags.
	Returns:
		list: A list of list, representing a transitional Viterbi matrix.
	
	"""
	gtProbability = turingSmoothing(biFreqs, uniFreqs)
	probs = [[0]*len(tagVocab)]*len(tagVocab)
	for key, value in biFreqs.items():
		(tag1, tag2) = key.split(WE[0])
		probs[tagVocab.index(tag1)][tagVocab.index(tag2)] = gtProbability(key)
	return probs

# Copied from assignment 3:
def turingSmoothing(Nfreq, N1freq):
	print("in HMM.py:turingSmoothing")
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