#!/usr/bin/python3

if __name__=="__main__":
	from dictionaire import Dict
	from .indexeddict import IndexedDict
	from .dictparser import DictParser
else:
	from .dict import Dict
	
class AnagramSet:
	def __init__(self, letters):
		self.letters=letters
		self.words=[]
	
	def addWord(self, word):
		if type(word) == list:
			self.words+=word
		else:
			self.words.append(word)
	
	def count(self):
		return len(self.words)
		
	def print(self):
		print(self.letters+" : "+str(sorted(self.words)))

class AnagramMaker:
	
	def __init__(self, dico):
		self.dict=dico
	
	def generateFromString(self, letters, minLetters=0):
		out=AnagramSet(letters)
		res=self.dict.findPossible(letters)
		out.addWord(res)
		return out



