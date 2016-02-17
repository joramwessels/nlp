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
	nGramProb = NGramProbabilities(N_freq, N_min_1_freq)
	question2(nGramProb, CPF, N)
	sentenceProb = sentenceProbabilities(NGramProb, N)
	question3(sentenceProb, SPF, N)
	question4(sentenceProbs, SP)

def frequency(freq, elem):
	"""Returns the value of the given key if present, or 0 otherwise.
	
	Args:
		freq (dict): A dictionary.
		elem: Any type of element of which the frequency is requested.
	Returns:
		int: The frequency of the element in the dicionary.
	
	"""
	if elem in list(freq.keys()):
		return freq[elem]
	else:
		return 0

def NGramProbabilities(N_freq, N_min_1_freq):
	"""Constructs a closure mapping N-grams to their probability.
	
	Args:
		N_freq (dict): A dictionary mapping N-grams to their frequency.
		N_min_1_freq (dict): A dictionary mapping (N-1)-grams to their frequency.
	Returns:
		func: A closure mapping N-grams to their probability.
	
	"""
	nGramProbs = {}
	def probability(nGram):
		split_line = nGram.strip().split(' ')
		NMin1Gram = ' '.join(split_line[:-1])
		PN = frequency(N_freq, nGram)
		PN1 = frequency(N_min_1_freq, NMin1Gram)
		if PN1 == 0: return 0
		return PN / PN1
	return probability

def SentenceProbabilities(NGramProb, N, start="START", stop="STOP"):
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
				prob *= NGramProb(" ".join(ngram))
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
	print("Question 1")
	freq = countNGrams(filename, N)
	sortedList = sorted(freq.items(), key=itemgetter(1))
	sortedList.reverse()
	sortedList.insert(0, ("Bigram", "Frequency"))
	prettyPrint(sortedList, M+1)

def question2(NGramProb, filename, N):
	"""Prints the probabilities of the N-grams in the given file.
	
	Args:
		NGramProbs (dict): A dictionary mapping N-grams to their probability.
		filename (str): The name of the N-grams file to test.
		N (int): The N value of the N-grams.
	
	"""
	if (NGramProb == None or filename == None): return
	print("Question 2")
	probabilities = []
	with open(filename, 'r') as file:
		for line in file:
			gram = line.strip().split(' ')
			if len(gram) == N:
				NMin1Gram = ' '.join(gram[:-1])
				NGram = ' '.join(gram)
				probabilities.append((NGram, NGramProb(NGram)))
	probabilities.insert(0, ("N-gram", "Probability"))
	prettyPrint(probabilities, len(probabilities))

def question3(sentenceProb, filename, N):
	"""Prints the probabilities of the sentences in the given file.
	
	Args:
		sentenceProb (func): A closure calculating the probability of a sentence.
		filename (str): The name of the file containing the test sentences.
		N (int): The N value of the N-grams.
	
	"""
	if (sentenceProb == None or filename == None): return
	print("Question 3")
	with open(filename, 'r') as file:
		printList = [(line, sentenceProb(line)) for line in file]
	printList.insert(0, ("Sentence", "Probability"))
	prettyPrint(printList, len(printList))

def question4(sentenceProb, scoredPermutations):
	"""Prints the probabilities of the permutations of set A and B.
	
	Args:
		sentenceProb (func): A closure calculating the probability of a sentence.
		scoredPermutations (bool): Whether to print this question or not.
	
	"""
	if (sentenceProb == None or not scoredPermutations): return
	print("Question 4")
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
	print()
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