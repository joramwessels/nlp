#! /usr/bin/python

class Buffer:
	"""Buffer object keeps track of the last N-1 words to form N-Grams.
	
	Args:
		N (int): The N value of the N-Grams.
		startSymbol (str): The symbol to represent a sentence start.
		stopSymbol (str): The symbol to represent a sentence stop.
	
	"""
	def __init__(self, N, startSymbol, stopSymbol):
		self.N = N
		self.start = startSymbol
		self.stop = stopSymbol
		self.flush()
	
	def flush(self):
		self.buffer = [self.start]*self.N
	
	def next(self, symbol):
		self.buffer.pop(0)
		self.buffer.insert(self.N-1, symbol)
		return self.buffer
	
	def end(self):
		return self.next(self.stop)

def nGramGenerator(sentence, N, start_symbol="START", stop_symbol="STOP"):
	"""Creates N-grams given a tokenized sentence.
	
	Args:
		sentence (list): A list with the words of the sentence.
		N (int): The N-value of the N-grams.
		start_symbol (str): (optional) The representation of a sentence start.
		stop_symbol (str): (optional) The representation of a sentence stop.
	Yields:
		str: The next N-Gram.
	
	"""
	buffer = Buffer(N, start_symbol, stop_symbol)
	sentence.extend([stop_symbol]*(N-1))
	yield ' '.join(buffer.next(buffer.start))
	for word in sentence:
		yield ' '.join(buffer.next(word))

def nGramsFromCorpus(filename, N, line_end='\n\n', word_end=' '):
	"""Returns a generator that yields n-grams from a file.
	
	Args:
		filename (str): The name of the corpus file.
		N (int): The size of the n-grams.
		line_end (str): (optional) The separator between sentences.
		word_end (str): (optional) The separator between words.
	Yields:
		list: The tokenized n-gram.
	
	"""
	with open(filename, 'r') as file:
		corpus = ''.join(file.readlines())
		sentences = corpus.split(line_end)
		for sent in sentences:
			if sent != '':
				sentence = [w for w in sent.strip().split(word_end) if w != '']
				ngrams = nGramGenerator(sentence, N)
				for gram in ngrams:
					yield gram

def countNGrams(filename, N):
	"""Counts the frequency the n-grams in a corpus.
	
	Args:
		filename (str): The name of the corpus file.
		N (int): The size of the n-grams.
		M (int): The amount of most frequent n-grams to print.
	Returns:
		dict: The frequencies, linked to the n-grams.
	
	"""
	ngrams = nGramsFromCorpus(filename, N)
	frequencies = {}
	for key in ngrams:
		if not key in frequencies.keys():
			frequencies[key] = 1
		else:
			frequencies[key] += 1
	return frequencies