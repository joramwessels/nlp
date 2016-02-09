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
	
	def stop(self):
		return self.next(self.stop)

def nGramGenerator(filename, N, start_symbol="START", stop_symbol="STOP"):
	"""Returns a generator that yields n-grams from a file.
	
	Args:
		filename (str): The name of the corpus file.
		N (int): The size of the n-grams.
	Yields:
		list: The tokenized n-gram.
	
	"""
	with open(filename, 'r') as file:
		buffer = Buffer(N, start_symbol, stop_symbol)
		try:
			while True:
				line = next(file)
				# End of paragraph
				if line.strip() == '':
					for i in range(N-1):
						yield buffer.stop()
					while line.strip() == '' and i < len(file):
						i += 1
						line = next(file)
					buffer.flush()
				# Reading paragraph
				sentence = line.strip().split(" ")
				for word in sentence:
					if word != '':
						yield buffer.next(word)
		except StopIteration:
			pass

def countNGrams(filename, N):
	"""Counts the frequency the n-grams in a corpus.
	
	Args:
		filename (str): The name of the corpus file.
		N (int): The size of the n-grams.
		M (int): The amount of most frequent n-grams to print.
	Returns:
		dict: The frequencies, linked to the n-grams.
	
	"""
	ngram = nGramGenerator(filename, N)
	frequencies = {}
	for gram in ngram:
		key = " ".join(gram)
		if not key in frequencies.keys():
			frequencies[key] = 1
		else:
			frequencies[key] += 1
	return frequencies