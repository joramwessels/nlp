#! /usr/bin/python

def probabilities(sentenceProb, filename, start="START", stop="STOP"):
	probabilities = {}
	with open(filename, 'r') as file:
		for line in file:
			probabilities[line.strip()] = sentenceProb(line)
	return probabilities