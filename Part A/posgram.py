#! /usr/bin/python

import sys

# internal 'line start' and 'line end' representation.
LS = "START/START"
LE = "STOP/STOP"

def main():
	tr, wt = viterbiMatrices(sys.argv[1], 2,
		line_ends=["./.", "======================================"],
		word_ends=[' ', '\n'], tag_del='/')
	print([(key, val) for key, val in list(tr.items())[:10]])
	print([(key, val) for key, val in list(wt.items())[:10]])

def sentenceToNgrams(sentence, N, tagDel, start_symbol=LS, stop_symbol=LE):
	sentence = [start_symbol]*N + sentence + [stop_symbol]*N
	sent = [word.split(tagDel)[1] for word in sentence if len(word.split(tagDel)) == 2]
	return [[sent[i+j] for j in range(N)] for i in range(len(sent)-N)]

def countTagNgrams(dict, sentence, N, tagDel, wordDel):
	"""Extends a dictionary that maps tag transitions to their frequency.
	
	Args:
		dict (dict): The dictionary to be extended.
		sentence (list): A sentence, as parsed by readPOSCorpus
		N (int): The N value of the transition N-grams.
		tagDel (str): The string functioning as POS tag delimiter.
		wordDel (str): The string functioning as word delimiter.
	
	"""
	ngrams = sentenceToNgrams(sentence, N, tagDel)
	for ngram in ngrams:
		gram = wordDel.join(ngram)
		if gram in dict.keys():
			dict[gram] += 1
		else:
			dict[gram] = 1

def countWordTags(dict, sentence):
	"""Extends a dictionary that maps word-tag couples to their frequency.
	
	Args:
		dict (dict): The dictionary to be extended.
		sentence (list): A sentence, as parsed by readPOSCorpus
	
	"""
	for word in sentence:
		if word in dict.keys():
			dict[word] += 1
		else:
			dict[word] = 1

def readPOSCorpus(filename, line_ends, word_ends):
	"""Reads a POS corpus from a file and parses the sentence structures.
	
	Args:
		filename (str): The name of the POS corpus file.
		line_ends (list): A list of all strings that indicate a line end.
		word_ends (list): A list of all strings that indicate a word end.
	Returns:
		list: A list of sentences, represented as a list of words.
	
	"""
	lineSep = "<LINESEP>"
	wordSep = "<WORDSEP>"
	file = open(filename, 'r')
	corpus = ''.join(file.readlines())
	for end in line_ends:
		corpus = corpus.replace(end, lineSep)
	file.close()
	sentences = corpus.split(lineSep)
	for i in range(len(sentences)):
		for end in word_ends:
			sentences[i] = sentences[i].replace(end, wordSep)
		sentences[i] = [w for w in sentences[i].split(wordSep) if w != '']
	sentences = [s for s in sentences if len(s) > 0]
	return sentences

def countPOSFreqs(filename, N, line_ends=["\n"], word_ends=[' '], tag_del='/'):
	print("in posgram.py:countPOSFreqs")
	"""Counts the frequencies of both word-tag couples and tag transitions.
	
	Args:
		filename (str): The name of the POS corpus file.
		N (int): The N value of the N-grams in POS tag transitions.
		line_ends (list): (optional) All strings that indicate a line end.
		word_ends (list): (optional) All strings that indicate a word end.
		tag_del (str): (optional) The string that separates words from tags.
	Returns:
		dict, dict: A dictionary mapping POS transitions to their frequency, as
					well as a dictionary mapping word-tags to their frequency.
	
	"""
	corpus = readPOSCorpus(filename, line_ends, word_ends)
	transitions = {}
	wordTags = {LS : len(corpus), LE : len(corpus)}
	for sentence in corpus:
		sent = [w for w in sentence if (tag_del in w) and (w[:1].isalnum())]
		countWordTags(wordTags, sent)
		countTagNgrams(transitions, sent, N, tag_del, word_ends[0])
	return transitions, wordTags

if __name__ == "__main__":
	main()