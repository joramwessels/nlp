#! /usr/bin/python
"""
NLP Part B
Amir Alnomani		10437797
Maurits Offerhaus	10400036
Joram Wessels		10631542
Compiles using Python version 3.5 with the following command:
	./b-step1.py -h [number] -v [number] -input [non-binarized] -output [binarized]
"""

import sys, argparse
from parse import binarizeTreebank

def main():
	h, v, input, output = parseArgs(sys.argv[1:])
	treebank = readTreebank(input)
	binarized = binarizeTreebank(treebank, h, v)
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
		for tree in binarized:
			out.write(treeToString(tree) + '\n\n')

def treeToString(tree):
	"""Converts the internal list representation of a tree into string format.
	
	Args:
		tree (list): The list of lists to be converted.
	Returns:
		str: The required string representation of the tree.
	
	"""
	if isinstance(tree, str): return tree
	return '(' + ' '.join([treeToString(x) for x in tree]) + ')'

def parseArgs(args):
	"""Parses the command line arguments.
	
	Args:
		args (list): The tokenized command line arguments.
	Returns:
		tuple: A tuple containing the input file and output file respectively.
	
	"""
	parser = argparse.ArgumentParser(description="Part B", conflict_handler='resolve')
	parser.add_argument(
		"-h",
		metavar='[number]',
		type=int,
		choices=[1,2],
		required=True,
		help="The order of horizontal Markovization.")
	parser.add_argument(
		"-v",
		metavar='[number]',
		type=int,
		choices=[1,2],
		required=True,
		help="The order of vertical Markovization.")
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
	return parsed.h, parsed.v, parsed.input, parsed.output

if __name__ == "__main__":
	main()