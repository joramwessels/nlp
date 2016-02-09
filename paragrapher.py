#! /usr/bin/python

import sys

def main():
	file = open(sys.argv[1], 'r')
	out = open(sys.argv[2], 'w')
	try:
		while True:
			line = next(file)
			if line.strip() == '':
				out.write("END ")
				while line.strip() == '':
					line = next(file)
				out.write("START ")
				out.write(line)
			else:
				out.write(line)
	except:
		pass
	file.close()
	out.close()

if __name__ == "__main__":
	main()