#! /usr/bin/python

"""
NLP Assignment 1
Amir Alnomani		10437797
Maurits Offerhaus	1040036
Joram Wessels		10631542

Compiles using Python version 3.5 with the following command:
	python assignment1.py -corpus [path] -n [value] -m [value]

Comulative frequencies:
	unigrams:	617091
	bigrams:	617091
	
"""

import sys, argparse, operator

def main():
	filename, N, M = parseArgs(sys.argv[1:])
	frequencies = countNGrams(filename, N, M)
	sortedList = sorted(frequencies.items(), key=operator.itemgetter(1))
	sortedList.reverse()
	prettyPrint(sortedList, M)

def countNGrams(filename, N, M):
	ngram = nGramGenerator(filename, N)
	frequencies = {}
	for gram in ngram:
		key = " ".join(gram)
		if not key in frequencies.keys():
			frequencies[key] = 1
		else:
			frequencies[key] += 1
	return frequencies

def nGramGenerator(filename, N):
	with open(filename, 'r') as file:
		buffer = [""]*N
		for line in file:
			sentence = line.strip().split(" ")
			for word in sentence:
				if (word != ''):
					buffer.pop(0)
					buffer.insert(N-1, word)
					yield buffer

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
		"-m",
		metavar='M',
		type=int,
		help="The amount of most probable n-grams to print.")
	parsed = parser.parse_args(args)
	return parsed.corpus[0], parsed.n, parsed.m

if __name__ == "__main__":
	main()