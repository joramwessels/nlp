#! /usr/bin/python

# TODO: divide-by-zero in probabilities, Turing Smoothing for N0?

from NGrams import countNGrams

class LanguageModel:
	
	def __init__(self, filename, N):
		"""A LanguageModel object builds a model using the frequencies of the
			N-grams and (N-1)-grams found in the corpus, and enables the
			calculation of the probability of any given N-gram using that model.
		"""
		self.Nfreq = countNGrams(filename, N)
		self.N1freq = countNGrams(filename, N-1)
		self.setNoSmoothing()
	
	def NGramProb(self, ngram):
		"""Calculates the probability of an N-gram using the language model.
		
		Args:
			ngram (str): The N-gram to be tested.
		Returns:
			float: The probability of the N-gram.
		
		"""
		return self.probability(ngram)
	
	def setNoSmoothing(self):
		"""Disables smoothing.
		
		"""
		self.probability = noSmoothing(self.Nfreq, self.N1freq)
	
	def setAdditiveSmoothing(self, alpha):
		"""Sets the smoothing method to Additive (Laplace) Smoothing.
		
		Args:
			alpha (int): The amount added to each frequency.
		
		"""
		self.probability = additiveSmoothing(self.Nfreq, self.N1freq, alpha)
	
	def setTuringSmoothing(self):
		"""Sets the smoothing method to Good Turing Smoothing.
		
		"""
		self.probability = turingSmoothing(self.Nfreq, self.N1freq)


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

def noSmoothing(Nfreq, N1freq):
	"""Returns a closure that calculates probability without smoothing.
	
	Args:
		Nfreq (dict): A dictionary mapping N-grams to their frequencies.
		N1freq (dict): A dictionary mapping (N-1)-grams to their frequencies.
	Returns:
		func: A function that calculates the probability of an N-gram.
	
	"""
	Ntotal = sum(Nfreq.values())
	N1total = sum(N1freq.values())
	def probability(ngram):
		n1gram = ngram.split(' ')[:-1]
		PN = frequency(Nfreq, ngram) / Ntotal
		PN1 = frequency(N1freq, n1gram) / N1total
		return PN / PN1
	return probability

def additiveSmoothing(Nfreq, N1freq, alpha):
	"""Returns a closure that calculates probability using Additive Smoothing.
	
	Args:
		Nfreq (dict): A dictionary mapping N-grams to their frequencies.
		N1freq (dict): A dictionary mapping (N-1)-grams to their frequencies.
		alhpa (int): The amount added to each frequency.
	Returns:
		func: A function that calculates the probability of an N-gram.
	
	"""
	Ntotal = sum(Nfreq.values()) + len(Nfreq.keys()) * alpha
	N1total = sum(N1freq.values()) + len(N1freq.keys()) * alpha
	def probability(ngram):
		n1gram = ngram.split(' ')[:-1]
		PN = (frequency(Nfreq, ngram) + alpha) / Ntotal
		PN1 = (frequency(N1freq, n1gram) + alpha) / N1total
		return PN / PN1
	return probability

def turingSmoothing(Nfreq, N1freq):
	"""Returns a closure that calculates probability using Turing Smoothing.
	
	Args:
		Nfreq (dict): A dictionary mapping N-grams to their frequencies.
		N1freq (dict): A dictionary mapping (N-1)-grams to their frequencies.
	Returns:
		func: A function that calculates the probability of an N-gram.
	
	"""
	Nvalues = list(Nfreq.values())
	N1values = list(N1freq.values())
	N = dict([(i, Nvalues.count(i)) for i in range(max(Nvalues))])
	N1 = dict([(i, N1values.count(i)) for i in range(max(N1values))])
	def probability(ngram):
		n1gram = ngram.split(' ')[:-1]
		C = frequency(Nfreq, ngram)
		Nc = frequency(N, C)
		Nc1 = frequency(N, C+1)
		PN = ((C + 1) * Nc1) / Nc
		C1 = frequency(N1freq, n1gram)
		N1c = frequency(N1, C1)
		N1c1 = frequency(N1, C1+1)
		PN = ((C1 + 1) * N1c1) / N1c
		return PN / PN1

def conditionalTuringSmoothing(Nfreq, N1freq, max_k=5):
	"""Returns a closure that calculates N-gram probability, using Turing
		Smoothing only when the frequency of the N-gram is less than max_k.
	
	Args:
		Nfreq (dict): A dictionary mapping N-grams to their frequencies.
		N1freq (dict): A dictionary mapping (N-1)-grams to their frequencies.
		max_k (int): (optional) The maximum N-gram frequency that is smoothed.
	Returns:
		func: A function that calculates the probability of an N-gram.
	
	"""
	turingProb = turingSmoothing(Nfreq, N1freq)
	normalProb = noSmoothing(Nfreq, N1freq)
	def probability(ngram):
		if frequency(Nfreq, ngram) <= max_k:
			return turingProb(ngram)
		else:
			return normalProb(ngram)
	return probability