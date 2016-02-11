#! /usr/bin/python

def probabilities(NGrams, NMin1Grams, conditional_prob_file, n):
	nGramProbs = {}
	with open(conditional_prob_file, 'r') as file:
		lines = file.readlines()

		for line in lines:
			original_line = line.strip()
			split_line = original_line.split()
			if len(split_line) != n:
				continue

			NMin1Gram = ' '.join(split_line[:n-1])
			if NMin1Gram in NMin1Grams.keys():
				NMin1Grams_freq = NMin1Grams[NMin1Gram]
			else:
				NMin1Grams_freq = 0.000000000000000001

			ngram = ' '.join(split_line[:n])
			if ngram in NGrams.keys():
				ngram_freq = NGrams[ngram]
			else:
				ngram_freq = 0

			nGramProb = ngram_freq / NMin1Grams_freq
			nGramProbs[ngram] = nGramProb
		
		#print(nGramProbs)

	return nGramProbs