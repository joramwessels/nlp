#! /usr/bin/python

"""
NLP Assignment 3
Amir Alnomani		10437797
Maurits Offerhaus	10400036
Joram Wessels		10631542

Compiles using Python version 3.5 with the following command:
	assignment3.py -train-corpus [path] -test-corpus [path]
					-n [value] -smoothing [no|add1|gt]

"""
import sys, argparse
from languageModel import LanguageModel
from NGrams import sentencesFromCorpus

def main():
	train, test, N, smoothing = parseArgs(sys.argv[1:])
	model = question1(train, N)
	question2(model, N, test)
	question3(model, N, test)

def question1(corpus, N=2):
	return LanguageModel(corpus, N)

def question2(model, N, test):
	print("\nAdd-1 Smoothing")
	testModel(model, N, test, "add1")

def question3(model, N, test):
	print("\nGood Turing Smoothing")
	testModel(model, N, test, "gt")

def testModel(model, N, test, smoothing, M=5):
	"""Prints the percentage of sentences in the test set with a probability
		of 0, as well as the first 5 of those sentences as well.
	
	Args:
		model (LanguageModel):
		N (int):
		test (str): The filename of the test corpus.
		smoothing (str): The flag of the smoothing method (no, add1, gt)
		M (int): (optional) The amount of 0-prob sentences printed.
	
	"""
	model.setSmoothing(smoothing)
	probability = sentenceProbabilities(model, N)
	sentences = sentencesFromCorpus(test, line_end='\n')
	zeroProb = [[sent] for sent in sentences if probability(sent) == 0]
	percentage = len(zeroProb) / len(sentences)
	print("Percentage of 0 probability: %.5f%%" %(percentage*100))
	zeroProb.insert(0, ["Sentences with zero probability:"])
	prettyPrint(zeroProb, M)

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

def prettyPrint(list, M):
	"""Prints the tuples in the list as columns, with the labels as the first tuple.
	
	Args:
		list (list): A list of tuples, which will be printed sequentially.
		M (int): The amount of list entries to print.
	
	"""
	slice = (list[:M] if M < len(list) else list)
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