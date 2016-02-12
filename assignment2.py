#! /usr/bin/python

"""
NLP Assignment 2
Amir Alnomani		10437797
Maurits Offerhaus	10400036
Joram Wessels		10631542

Compiles using Python version 3.5 with the following command:
	assignment2.py -corpus [path] -n [value] -conditional-prob-file [path]
		-sequence-prob-file [path] -scored-permutations [path]

"""
import sys, argparse, operator
from NGrams import nGramGenerator, countNGrams
import question2_2 as q2
import question2_3 as q3
import question2_4 as q4

def main():
	parsed = parseArgs(sys.argv[1:])
	corpus = parsed["corpus"][0]
	CPF = parsed["conditional_prob_file"][0]
	SPF = parsed["sequence_prob_file"][0]
	SP = parsed["scored_permutations"][0]
	N = parsed["n"]
	question1(corpus)
	
	# Counting N- and (N-1)-Grams
	N_freq = countNGrams(corpus, N)
	N_min_1_freq = countNGrams(corpus, N-1)
	
	# Calculating probabilities
	nGramProbs = probabilities(N_freq, N_min_1_freq)
	question2(nGramProbs, CPF, N)
	sentenceProb = sentenceProbabilities(NGramProbs, N)
	question3(sentenceProb, SPF, N)
	permutations = question4(sentenceProbs, SP)
	print(nGramProbs, sentenceProbs, permutations)

def NGramProbabilities(N_freq, N_min_1_freq):
	NGramProbs = {}
	return NGramProbs

def SentenceProbabilities(NGramProbs, N, start="START", stop="STOP"):
	def func(line):
		words = [start]*(N-1) + line.strip().split(' ') + [stop]*(N-1)
		words = [word for word in words if not word == '']
		ngrams = [words[i:(i+N)] for i in range(len(words)-(N-1))]
		prob = 1
		for ngram in ngrams:
			try:
				prob *= NGramProbs[" ".join(ngram)]
			except KeyError:
				prob = 0
		return prob
	return func

def question1(filename, N=2, M=10):
	freq = countNGrams(filename, N)
	sortedList = sorted(freq.items(), key=operator.itemgetter(1))
	sortedList.reverse()
	sortedList.insert(0, ("Bigram", "Frequency"))
	prettyPrint(sortedList, M+1)

def question2(NGramProbs, filename, N):
	if (NGramProbs == None or filename == None): return
	q2.probabilities(NGramProbs, filename, N)

def question3(sentenceProb, filename, N):
	if (sentenceProb == None or filename == None): return
	
	with open(filename, 'r') as file:
		probabilities = [sentenceProb(line) for line in file]
	return probabilities

def question4(sentenceProb, filename):
	if (sentenceProb == None or filename == None): return
	
	setA = ["know","I","opinion","do","be","your","not","may","what"]
	setB = ["I","do","not","know"]
	PermsOfA = list(itertools.permutations(setA))
	PermsOfB = list(itertools.permutations(setB))
	
	prob = {}
	for permA,PermB in zip(PermsOfA,PermsOfB):
		permA = " ".join(permA)
		prob[permA] = sentenceProbs(permA)
		permB = " ".join(permB)
		prob[permB] = sentenceProbs(permB)
	return prob

def prettyPrint(list, M):
	slice = list[:M]
	lengths = [max([len(str(tuple[i])) for tuple in slice]) for i in range(len(list[0]))]
	for row in slice:
		for i in range(len(row)-1):
			print(row[i], end='')
			[print(' ', end='') for j in range(lengths[i] + 1 - len(row[i]))]
		print(row[len(row)-1])

def parseArgs(args):
	"""Parses the arguments using argparse.
	
	Args:
		args (list): The command line arguments, excluding the program name.
	Returns:
		Namespace: The parsed arguments.
	
	"""
	name = "Assignment 1"
	parser = argparse.ArgumentParser(description=name)
	parser.add_argument(
		"-corpus",
		metavar='C',
		type=str,
		nargs=1,
		help="The path to the corpus.")
	parser.add_argument(
		"-n",
		metavar='N',
		type=int,
		help="The 'n' order of the n-grams.")
	parser.add_argument(
		"-conditional-prob-file",
		metavar='CO',
		type=str,
		nargs=1,
		required=False,
		default=[None],
		help="The path to the conditional probability file.")
	parser.add_argument(
		"-sequence-prob-file",
		metavar='SE',
		type=str,
		nargs=1,
		required=False,
		default=[None],
		help="The path to the sequence probability file.")
	parser.add_argument(
		"-scored-permutations",
		metavar='SC',
		type=str,
		nargs=1,
		required=False,
		default=[None],
		help="The path to the scored permutations file.")
	parsed = vars(parser.parse_args(args))
	return parsed

if __name__ == "__main__":
	main()
