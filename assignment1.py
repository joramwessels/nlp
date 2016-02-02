#! /usr/bin/python

import sys, argsparse

def main():
	args = parseArgs(sys.argv[1:])
	

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
		help="The amount of most probable n-grams to print.")
	parsed = parser.parse_args(argv)
	return parsed.corpus, parsed.n, parsed.m

if __name__ == "__main__":
	main()