#! /usr/bin/python

"""
NLP Assignment 1
Amir Alnomani		10437797
Maurits Offerhaus	1040036
Joram Wessels		10631542

Compiles using Python version 3.5 with the following command:
	python assignment1.py -corpus [path] -n [value] -m [value]

Most frequent n-grams:
	Unigram                         Frequency
	the                             | 20829
	to                              | 20042
	and                             | 18331
	of                              | 17949
	a                               | 11135
	her                             | 11007
	I                               | 10381
	was                             | 9409
	in                              | 9182
	it                              | 7573

	Bigram                          Frequency
	of the                          | 2507
	to be                           | 2233
	in the                          | 1917
	I am                            | 1366
	of her                          | 1264
	to the                          | 1142
	it was                          | 1010
	had been                        | 995
	she had                         | 978
	to her                          | 964

	Trigram                         Frequency
	I do not                        | 378
	I am sure                       | 366
	in the world                    | 214
	she could not                   | 202
	would have been                 | 189
	I dare say                      | 174
	as soon as                      | 173
	a great deal                    | 173
	it would be                     | 171
	could not be                    | 155

Comulative frequencies:
	unigrams:	617091
	bigrams:	617091
	trigrams:	617091
	
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

def nGramGenerator(filename, N):
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
		required=False,
		default=5,
		help="The amount of most probable n-grams to print.")
	parsed = parser.parse_args(args)
	return parsed.corpus[0], parsed.n, parsed.m

if __name__ == "__main__":
	main()