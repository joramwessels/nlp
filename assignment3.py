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
	model = question1(train, N)
	model.setSmoothing(smoothing)
	print("Test an N-gram:\n >>", end='')
	for ngram in sys.stdin:
		print("Probability: %.5f" %(model.NGramProb(ngram)), end='\n >>')

def question1(corpus, N):
	return LanguageModel(train, N)

def question2(model, N, test):
	pass

def question3():
	pass

def sentenceProbabilities(model, N, start="START", stop="STOP"):
	"""Constructs a closure calculating sentence probabilities.
	
	Args:
		model (LanguageModel): A language model able to calculate N-gram probs.
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
			prob *= model.NGramProb(" ".join(ngram))
		return prob
	return func

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
		required=False,
		default='no',
		choices=['no', 'add1', 'gt'],
		help="The smoothing method applied to the predictions.")
	parsed = vars(parser.parse_args(args))
	return parsed["train_corpus"], parsed["test_corpus"], parsed["n"], parsed["smoothing"]

if __name__ == "__main__":
	main()