#! /usr/bin/python

"""
NLP Assignment 2
Amir Alnomani		10437797
Maurits Offerhaus	1040036
Joram Wessels		10631542

Compiles using Python version 3.5 with the following command:
	assignment2.py -corpus [path] -n [value] -conditional-prob-file [path]

"""
import sys, argparse, operator
import question2_2 as q2
import question2_3 as q3
import question2_4 as q4

def main():
	parsed = parseArgs(sys.argv[1:])
	N_freq = countNGrams(parsed["corpus"][0], parsed["n"])
	N_min_1_freq = countNGrams(parsed["corpus"][0], parsed["n"]-1)
	sortedN = sorted(N_freq.items(), key=operator.itemgetter(1))
	sortedN.reverse()
	sortedN_min_1 = sorted(N_min_1_freq.items(), key=operator.itemgetter(1))
	sortedN_min_1.reverse()
	nGramProbs = question2(sortedN, sortedN_min_1, parsed["conditional_prob_file"][0])
	sentenceProbs = question3(nGramProbs, parsed["sequence_prob_file"][0])
	permutations = question4(sentenceProbs, parsed["scored_permutations"][0])
	print(nGramProbs, sentenceProbs, permutations)

def question2(NGrams, NMin1Grams, filename):
	if filename == None:
		return {}
	return q2.probabilities(NGrams, NMin1Grams, filename)

def question3(NGramProbs, filename):
	if filename == None:
		return {}
	return q3.probabilities(NGramProbs, filename)

def question4(sentenceProbs, filename):
	if filename == None:
		return {}
	return q4.probabilities(sentenceProbs, filename)

def countNGrams(filename, N):
	"""Counts the frequency the n-grams in a corpus.
	
	Args:
		filename (str): The name of the corpus file.
		N (int): The size of the n-grams.
		M (int): The amount of most frequent n-grams to print.
	Returns:
		dict: The frequencies, linked to the n-grams.
	
	"""
	ngram = nGramGenerator(filename, N)
	frequencies = {}
	for gram in ngram:
		key = " ".join(gram)
		if not key in frequencies.keys():
			frequencies[key] = 1
		else:
			frequencies[key] += 1
	return frequencies

def nGramGenerator(filename, N, start_symbol="START", stop_symbol="STOP"):
	"""Returns a generator that yields n-grams from a file.
	
	Args:
		filename (str): The name of the corpus file.
		N (int): The size of the n-grams.
	Yields:
		list: The tokenized n-gram.
	
	"""
	with open(filename, 'r') as file:
		buffer = [""]*N
		for line in file:
			sentence = line.strip().split(" ")
			for word in sentence:
				if "" in buffer:
					buffer.pop(0)
					buffer.insert(N-1, word)
				if not word in ["", start_symbol, stop_symbol]:
					buffer.pop(0)
					buffer.insert(N-1, word)
					yield buffer
				if word == stop_symbol:
					buffer = [""]*N

def prettyPrint(list, M):
	print("NGram\t\t\t\tFrequency")
	for i in range(M):
		print(list[i][0],"\t\t\t\t|",list[i][1])

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