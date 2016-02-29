#! /usr/bin/python

import sys

def main():
	tr, wt = viterbiMatrices(sys.argv[1], 2,
		line_ends=["./.", "======================================"],
		word_ends=[' ', '\n'], tag_del='/')
	print([(key, val) for key, val in tr.items()])
	print([(key, val) for key, val in wt.items()])

def sentenceToNgrams(sentence, N, start_symbol="<s>", stop_symbol="</s>"):
	sent = [start_symbol]*N + sentence + [stop_symbol]*N
	return [[sent[i+j] for j in range(N)] for i in range(len(sent)-N)]

def countTagNgrams(dict, sentence, N):
	ngrams = sentenceToNgrams(sentence, N)
	for ngram in ngrams:
		gram = ' '.join(ngram)
		if gram in dict.keys():
			dict[gram] += 1
		else:
			dict[gram] = 1

def countWordTags(dict, sentence):
	for word in sentence:
		if word in dict.keys():
			dict[word] += 1
		else:
			dict[word] = 1

def readPOSCorpus(filename, line_ends, word_ends):
	lineSep = "<LINESEP>"
	wordSep = "<WORDSEP>"
	file = open(filename, 'r')
	corpus = ''.join(file.readlines())
	[corpus.replace(end, lineSep) for end in line_ends]
	file.close()
	sentences = corpus.split(lineSep)
	print(corpus[:100])
	for i in range(len(sentences)):
		[sentences[i].replace(end, wordSep) for end in word_ends]
		sentences[i] = sentences[i].split(wordSep)
	return sentences

def viterbiMatrices(filename, N, line_ends=["\n"], word_ends=[' '], tag_del='/'):
	transitions = {}
	wordTags = {}
	corpus = readPOSCorpus(filename, line_ends, word_ends)
	for sentence in corpus:
		sent = [w for w in sentence if (tag_del in w) and (w[:1].isalnum())]
		countWordTags(wordTags, sent)
		countTagNgrams(transitions, sent, N)
	return transitions, wordTags

if __name__ == "__main__":
	main()