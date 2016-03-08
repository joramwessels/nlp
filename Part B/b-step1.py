#! /usr/bin/python
"""
NLP Part A
Amir Alnomani		10437797
Maurits Offerhaus	10400036
Joram Wessels		10631542
Compiles using Python version 3.5 with the following command:
	./b-step1.py -input [non-binarized]	-output [binarized]
"""

import sys, argparse
from binarizer import parseTreebank

def main():
	input, output = parseArgs(sys.argv[1:])
	binarized = parseTreebank(input)
	saveBinarized(binarized, output)

def saveBinarized(binarized, output):
	"""Saves the parsed treebank in the output location.
	
	Args:
		binarized (list): 
		output (str): The path to the output file.
	
	"""
	with open(output, 'w') as out:
		for bin in binarized:
			out.write(bin + '\n')

def parseArgs(args):
	"""Parses the command line arguments.
	
	Args:
		args (list): The tokenized command line arguments.
	Returns:
		tuple: A tuple containing the input file and output file respectively.
	
	"""
	parser = argparse.ArgumentParser(description="Part B1")
	parser.add_argument(
		"-input",
		metavar='[path]',
		type=str,
		required=True,
		help="The path to the non-binarized file.")
	parser.add_argument(
		"-output",
		metavar='[path]',
		type=str,
		required=True,
		help="The path to the file in which to save the binary trees.")
	parsed = parser.parse_args(args)
	return parsed.input, parsed.output

if __name__ == "__main__":
	main()