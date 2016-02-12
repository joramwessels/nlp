#! /usr/bin/python

"""
NLP Assignment 2
Amir Alnomani		10437797
Maurits Offerhaus	10400036
Joram Wessels		10631542

Compiles using Python version 3.5 with the following command:
	assignment2.py -corpus [path] -n [value] -conditional-prob-file [path]
		-sequence-prob-file [path] -scored-permutations

"""
import sys, argparse
from operator import itemgetter
from NGrams import countNGrams

def main():
	parsed = parseArgs(sys.argv[1:])
	corpus = parsed["corpus"][0]
	CPF = parsed["conditional_prob_file"][0]
	SPF = parsed["sequence_prob_file"][0]
	SP = parsed["scored_permutations"]
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
	question4(sentenceProbs, SP)

def NGramProbabilities(N_freq, N_min_1_freq):
	"""Constructs a dictionary mapping N-grams to their probability.
	
	Args:
		N_freq (dict): A dictionary mapping N-grams to their frequency.
		N_min_1_freq (dict): A dictionary mapping (N-1)-grams to their frequency.
	Returns:
		dict: A dictionary mapping N-grams to their probability.
	
	"""
	NGramProbs = {}
	# TODO
	return NGramProbs

def SentenceProbabilities(NGramProbs, N, start="START", stop="STOP"):
	"""Constructs a closure calculating sentence probabilities.
	
	Args:
		NGramProbs (dict): A dictionary mapping N-grams to their probability.
		N (int): The N value of the N-grams.
		start (str): (optional) The symbol for the start of a sentence.
		stop (str): (optional) The symbol for the end of a sentence.
	Returns:
		func: A closure calculating the probability of a sentence.
	
	"""
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
	"""Prints the M most frequent N-grams.
	
	Args:
		filename (str): The name of the corpus to extract N-grams from.
		N (int): (optional) The N value of the N-grams (bigrams are requested)
		M (int): (optional) The amount of most N-grams printed (10 is requested)
	
	"""
	freq = countNGrams(filename, N)
	sortedList = sorted(freq.items(), key=operator.itemgetter(1))
	sortedList.reverse()
	sortedList.insert(0, ("Bigram", "Frequency"))
	prettyPrint(sortedList, M+1)

def question2(NGramProbs, filename, N):
	"""Prints the probabilities of the N-grams in the given file.
	
	Args:
		NGramProbs (dict): A dictionary mapping N-grams to their probability.
		filename (str): The name of the N-grams file to test.
		N (int): The N value of the N-grams.
	
	"""
	if (NGramProbs == None or filename == None): return
	# TODO
	printList.insert(0, ("N-gram", "Probability"))
	prettyPrint(printList, len(printList))

def question3(sentenceProb, filename, N):
	"""Prints the probabilities of the sentences in the given file.
	
	Args:
		sentenceProb (func): A closure calculating the probability of a sentence.
		filename (str): The name of the file containing the test sentences.
		N (int): The N value of the N-grams.
	
	"""
	if (sentenceProb == None or filename == None): return
	
	with open(filename, 'r') as file:
		probabilities = [(line, sentenceProb(line)) for line in file]
	printList.insert(0, ("Sentence", "Probability"))
	prettyPrint(printList, len(printList))

def question4(sentenceProb, scoredPermutations):
	"""Prints the probabilities of the permutations of set A and B.
	
	Args:
		sentenceProb (func): A closure calculating the probability of a sentence.
		scoredPermutations (bool): Whether to print this question or not.
	
	"""
	if (sentenceProb == None or not scoredPermutations): return
	
	setA = ["know","I","opinion","do","be","your","not","may","what"]
	setB = ["I","do","not","know"]
	PermsOfA = list(itertools.permutations(setA))
	PermsOfB = list(itertools.permutations(setB))
	
	prob = [' '.join(permA) for permA in PermsOfA]
	prob.extend([' '.join(permB) for permB in PermsOfB])
	printList = [(perm, sentenceProb(perm)) for perm in prob]
	printList.insert(0, ("Permutation", "Probability"))
	prettyPrint(printList, len(printList))

def prettyPrint(list, M):
	"""Prints the tuples in the list as columns, with the labels as the first tuple.
	
	Args:
		list (list): A list of tuples, which will be printed sequentially.
		M (int): The amount of list entries to print.
	
	"""
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
		metavar='[path]',
		type=str,
		nargs=1,
		required=True,
		help="The path to the corpus.")
	parser.add_argument(
		"-n",
		metavar='[value]',
		type=int,
		required=True,
		help="The 'n' order of the n-grams.")
	parser.add_argument(
		"-conditional-prob-file",
		metavar='[path]',
		type=str,
		nargs=1,
		required=False,
		default=[None],
		help="The path to the conditional probability file.")
	parser.add_argument(
		"-sequence-prob-file",
		metavar='[path]',
		type=str,
		nargs=1,
		required=False,
		default=[None],
		help="The path to the sequence probability file.")
	parser.add_argument(
		"-scored-permutations",
		action='store_true',
		required=False,
		help="The path to the scored permutations file.")
	parsed = vars(parser.parse_args(args))
	return parsed

if __name__ == "__main__":
	main()