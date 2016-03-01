#! /usr/bin/python

"""
NLP Part A
Amir Alnomani		10437797
Maurits Offerhaus	10400036
Joram Wessels		10631542
Compiles using Python version 3.5 with the following command:
	assignmentA.py -train-set [path] -test-set [path]
					-test-set-predicted [path] -smoothing [yes|no]
"""
import sys, argparse
import numpy as np
from HMM import HMM
from posgram import readPOSCorpus

LE = ["./.", "======================================"]
WE = [' ', '\n']
TD = '/'

def main():
	train, test, predicted, smoothing = parseArgs(sys.argv[1:])
	model = trainModel(train, smoothing)
	acc = testModel(model, test, predicted)
	print("Accuracy: %.5f" %acc)

def trainModel(corpus, smoothing):
	# build viterbi matrices
	model = HMM(corpus, smoothing)
	# closure using viterbi algorithm
	def tagger(sentence):
		if sentence == []: return []
		print("Tagging sentence...")
		tagSeq = []
		transProbs = model.getTransitionProbs() #probs[tagVocab.index(tag1)][tagVocab.index(tag2)]
		observProbs = model.getTagProbs() #word tagindex
		tagOrder = model.getTagVocab()
		wordOrder = model.getWordVocab()
		#print(len(observProbs),len(wordOrder))
		sTransProbs = np.array(transProbs[tagOrder.index('START')])
		npTransProbs = np.array(transProbs)
		
		N = len(tagOrder) #amount of tags
		T = len(sentence) #amount of word observations
		viterbi = np.zeros((N,T))
		print("sentence",sentence)
		viterbi[:,0] = sTransProbs*np.array(observProbs[wordOrder.index(sentence[0])])
		
		tagSeq.append(tagOrder[np.argmax(viterbi[:,0])]) # adds tag with the highest probability
		
		for t in range(1,T):
			for s in range(0,N):
				try:
					viterbi[s,t] = np.max(viterbi[:,t-1]*npTransProbs[:,s])*observProbs[wordOrder.index(sentence[t])][s]
				except ValueError:
					print(sentence[t])
			tagSeq.append(tagOrder[np.argmax(viterbi[:,t])])
		print("sentence: ",sentence, "tag sequence: ", tagSeq)
		return tagSeq
	# return closure
	return tagger

def viterbi(trans, ngram):
	pass

def testModel(model, testCorpus, predictions):
	correct = []
	with open(predictions, 'w') as out:
		sentences = readPOSCorpus(testCorpus, LE, WE)
		for sent in sentences:
			if len(sent) > 15 or sent == []: continue
			words = []
			tags = []
			for token in sent:
				spl = token.split(TD)
				if len(spl) != 2 or not spl[0].isalnum(): continue
				words.append(spl[0])
				tags.append(spl[1])
			predictions = model(words)
			out.write(' '.join(tags) + '\n')
			for i in range(len(tags)):
				if tags[i] == predictions[i]:
					correct.append(1)
				else:
					correct.append(0)
	print(correct)
	return np.mean(correct)

def parseArgs(args):
	"""Parses the arguments using argparse.
	
	Args:
		args (list): The command line arguments, excluding the program name.
	Returns:
		Namespace: The parsed arguments.
	
	"""
	name = "Part A"
	parser = argparse.ArgumentParser(description=name)
	parser.add_argument(
		"-train-set",
		metavar='[path]',
		type=str,
		required=True,
		help="The path to the train corpus.")
	parser.add_argument(
		"-test-set",
		metavar='[path]',
		type=str,
		required=True,
		help="The path to the test corpus.")
	parser.add_argument(
		"-test-set-predicted",
		metavar='[path]',
		type=str,
		required=True,
		help="The path to the new predictions.")
	parser.add_argument(
		"-smoothing",
		metavar='[yes|no]',
		type=str,
		required=False,
		default='no',
		choices=['yes', 'no'],
		help="The smoothing method applied to the predictions.")
	parsed = parser.parse_args(args)
	train = parsed.train_set
	test = parsed.test_set
	predicted = parsed.test_set_predicted
	smoothing = (True if parsed.smoothing == 'yes' else False)
	return train, test, predicted, smoothing

if __name__ == "__main__":
	main()

"""
train
	read file
	seperate sentences
	parse sentence
	word/tag frequencies
	tag bigram frequencies
	tag bigram probabilities
	Viterbi matrices
	closure using viterbi algorithm
test
	read file
	seperate sentences
	parse sentence
	check length > 15
	tag sentence
	save tags
	calculate accuracy
"""
