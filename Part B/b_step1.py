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
	treebank = readTreebank(input)
	binarized = parseTreebank(treebank)
	saveBinarized(binarized, output)

def readTreebank(input):
	"""Reads and parses all trees in the treebank.
	
	Args:
		input (str): The path to the file containing the treebank.
	Returns:
		list: A list of trees, represented as lists of lists.
	
	"""
	with open(input, 'r') as file:
		return [parseLine(line) for line in file if line.strip() != '']

def parseLine(line, sym_open='(', sym_close=')', delimiter=' '):
	"""Converts a tree string into a list of lists.
	
	Args:
		line (str): The tree represented as a list.
	Returns:
		list: A list of lists, according to the input tree.
	
	"""
	stack = []
	for char in line:
		if char == delimiter:
			stack[-1].append('')
		elif char == sym_open:
			if len(stack) > 0: stack[-1].pop()
			stack.append([''])
		elif char == sym_close and len(stack) > 1:
			stack[-2].append(stack.pop())
		elif char == sym_close and len(stack) == 1:
			return stack[0]
		else:
			stack[-1][-1] += char

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