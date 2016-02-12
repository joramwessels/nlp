#! /usr/bin/python

"""
NLP Assignment 3
Amir Alnomani		10437797
Maurits Offerhaus	10400036
Joram Wessels		10631542

Compiles using Python version 3.5 with the following command:
	assignment2.py -train-corpus [path] -test-corpus [path]
					-n [value] -smoothing [no|add1|gt]

"""
import sys, argparse
from languageModel import LanguageModel

def main():
	train, test, N, smoothing = parseArgs(sys.argv[1:])
	model = LanguageModel(train, N)
	model.setSmoothing(smoothing)
	print("Test an N-gram:\n >>", end='')
	for ngram in sys.stdin:
		print("Probability: %.5f" %(model.NGramProb(ngram)), end='\n >>')

def parseArgs(args):
	"""Parses the arguments using argparse.
	
	Args:
		args (list): The command line arguments, excluding the program name.
	Returns:
		Namespace: The parsed arguments.
	
	"""
	name = "Assignment 3"
	parser = argparse.ArgumentParser(description=name)
	parser.add_argument(
		"-train-corpus",
		metavar='[path]',
		type=str,
		required=True,
		help="The path to the train corpus.")
	parser.add_argument(
		"-test-corpus",
		metavar='[path]',
		type=str,
		required=True,
		help="The path to the test corpus.")
	parser.add_argument(
		"-n",
		metavar='[value]',
		type=int,
		required=True,
		help="The 'n' order of the n-grams.")
	parser.add_argument(
		"-smoothing",
		metavar='[no|add1|gt]',
		type=str,
		required=True,
		default='no',
		choices=['no', 'add1', 'gt'],
		help="The smoothing method applied to the predictions.")
	parsed = vars(parser.parse_args(args))
	return parsed["train_corpus"], parsed["test_corpus"], parsed["n"], parsed["smoothing"]

if __name__ == "__main__":
	main()