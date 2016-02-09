#! /usr/bin/python

def probabilities(NGrams, NMin1Grams, conditional_prob_file):
	conditional_prob = dict()
	lines = conditional_prob_file.readlines()

	for line in lines:
		split_line = line.split()
		if len(split_line) != n:
			continue

		NMin1Grams = ' '.join(split_line[:n-1])
		if ngram in ngram_dict:
			NMin1Grams_freq = n_1gram_dict[NMin1Grams]
		else:
			NMin1Grams_freq = 0

		ngram = ' '.join(split_line[:n])
		if ngram in ngram_dict:
			ngram_freq = ngram_dict[ngram]
		else:
			ngram_freq = 0

		nGramProbs = ngram_freq / n_1gram_freq
		conditional_prob[' '.join(split_line)] = nGramProbs

	print(conditional_prob)