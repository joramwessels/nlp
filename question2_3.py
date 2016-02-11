#! /usr/bin/python

def probabilities(NGramProbs, filename, N, start="START", stop="STOP"):
	probabilities = {}
	with open(filename, 'r') as file:
		for line in file:
			words = [start]*(N-1) + line.strip().split(' ') + [stop]*(N-1)
			words = [word for word in words if not word == '']
			ngrams = [words[i:(i+N)] for i in range(len(words)-(N-1))]
			prob = 1
			for ngram in ngrams:
				try:
					prob *= NGramProbs[" ".join(ngram)]
				except KeyError:
					prob = float('NaN')
			probabilities[line.strip()] = prob
	return probabilities