from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'

class Directory:
	def __init__(self, parent=None):
		self.subdirectories = {}
		self.files = []
		self.parent = parent
	
	def size(self):
		out = 0
		for name in self.subdirectories:
			out += self.subdirectories[name].size()
		
		for file in self.files:
			out += file.size
		
		return out

	def add_file(self, file):
		self.files.append(file)

	def add_directory(self, name):
		assert name not in self.subdirectories
		self.subdirectories[name] = Directory(self)

	def iterate_directories(self):
		yield self
		for name in self.subdirectories:
			for directory in self.subdirectories[name].iterate_directories():
				yield directory

class File:
	def __init__(self, name, size):
		self.name = name
		self.size = size


def main():
	root = Directory()
	current_directory = root
	with open(DATA_FILE, 'r') as file:
		for line in file:
			elements = line.split()
			if elements[0] == '$':
				if elements[1] == 'cd':
					if elements[2] == '/':
						current_directory = root
					elif elements[2] == '..':
						current_directory = current_directory.parent
					else:
						current_directory = current_directory.subdirectories[elements[2]]
				else:
					assert elements[1] == 'ls' and len(elements) == 2
			elif elements[0] == 'dir':
				current_directory.add_directory(elements[1])
			else:
				current_directory.add_file(File(elements[1], int(elements[0])))
	
	min_size = root.size() - 40000000
	best = 30000000
	
	out1 = 0
	for directory in root.iterate_directories():
		size = directory.size()
		if size <= 100000:
			out1 += size
		if size >= min_size and size < best:
			best = size


	return (out1, best)

print(main())
