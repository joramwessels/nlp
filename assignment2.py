#! /usr/bin/python

"""
NLP Assignment 2
Amir Alnomani		10437797
Maurits Offerhaus	1040036
Joram Wessels		10631542

Compiles using Python version 3.5 with the following command:
	python assignment2.py

"""
import sys, argparse, operator

def main():
	filename, N, M = parseArgs(sys.argv[1:])
	frequencies = countNGrams(filename, N, M)
	sortedList = sorted(frequencies.items(), key=operator.itemgetter(1))
	sortedList.reverse()
	prettyPrint(sortedList, M)

def countNGrams(filename, N, M):
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
		"-m",
		metavar='M',
		type=int,
		required=False,
		default=5,
		help="The amount of most probable n-grams to print.")
	parsed = parser.parse_args(args)
	return parsed.corpus[0], parsed.n, parsed.m

if __name__ == "__main__":
	main()