#! /usr/bin/python

import sys

def main():
	tr, wt = viterbiMatrices(sys.argv[1], 2,
		line_ends=["./.", "======================================"],
		word_ends=[' ', '\n'], tag_del='/')
	print([(key, val) for key, val in list(tr.items())[:10]])
	print([(key, val) for key, val in list(wt.items())[:10]])

def sentenceToNgrams(sentence, N, start_symbol="<s>", stop_symbol="</s>"):
	sent = [start_symbol]*N + sentence + [stop_symbol]*N
	return [[sent[i+j] for j in range(N)] for i in range(len(sent)-N)]

def countTagNgrams(dict, sentence, N, tagDel):
	sentence = [word.split(tagDel)[1] for word in sentence]
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

def viterbiMatrices(filename, N, line_ends=["\n"], word_ends=[' '], tag_del='/'):
	transitions = {}
	wordTags = {}
	corpus = readPOSCorpus(filename, line_ends, word_ends)
	for sentence in corpus:
		sent = [w for w in sentence if (tag_del in w) and (w[:1].isalnum())]
		countWordTags(wordTags, sent)
		countTagNgrams(transitions, sent, N, tag_del)
	return transitions, wordTags

if __name__ == "__main__":
	main()