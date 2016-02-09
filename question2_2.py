#! /usr/bin/python

def probabilities(NGrams, NMin1Grams, conditional_prob_file, n):
	nGramProbs = []
	with open(conditional_prob_file, 'r') as file:
		lines = file.readlines()

		for line in lines:
			original_line = line.strip()
			split_line = original_line.split()
			if len(split_line) != n:
				continue

			NMin1Gram = ' '.join(split_line[:n-1])
			print(NMin1Gram)
			if NMin1Gram in NMin1Grams:
				NMin1Grams_freq = NMin1Grams[original_line]
				print("penis")
			else:
				NMin1Grams_freq = 1

			ngram = ' '.join(split_line[:n])
			if ngram in NGrams:
				ngram_freq = NGrams[ngram]
			else:
				ngram_freq = 2

			nGramProb = ngram_freq / NMin1Grams_freq
			nGramProbs.append(nGramProb)

		#print(nGramProbs)

	return nGramProbs