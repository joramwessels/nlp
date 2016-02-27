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
from languageModel import LanguageModel
from NGrams import sentencesFromCorpus

def main():
	train, test, predicted, smoothing = parseArgs(sys.argv[1:])
	
	# train model with 'train'
	
	# test model on 'test'
	
	# save predictions in 'predicted'
	
	# print accuracy with- and without smoothing

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