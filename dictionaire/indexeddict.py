#!/usr/bin/python3

#from dictionaire import *
import json
import unidecode
import sys


def infstr(a, b):
	return strcmp(a,b)<0
	
def supstr(a, b):
	return strcmp(a,b)>0
	
def eqstr(a, b):
	return strcmp(a,b)==0

# a<b  -> -1
# a==b -> 0
# a>b  -> 1
def strcmp(a, b):
	a=unidecode.unidecode(a.lower())
	b=unidecode.unidecode(b.lower())
	la=len(a)
	lb=len(b)
	min=la if la<lb else lb
	for i in range(min):
		if a[i]<b[i]: return -1
		if a[i]>b[i]: return 1
	if la<lb: return -1
	if la>lb: return 1
	return 0

# si b est un sous anagram de a
# isSubAnagram("chien", "chiens") : True
# isSubAnagram("chiens", "chien") : False
def isSubAnagram(possible, word):
	tmp=""+possible
	for c in word:
		if not (c in tmp): return False
		tmp=tmp.replace(c, '', 1)
	return True
		

class IndexList:
	def __init__(self):
		self.list=[]
		
	def addWord(self, word):
		if len(self.list)==0:
			self.list.append(word)
		elif infstr(word, self.list[0]):
			self.list.insert(0, word)
		else:
			for i in range(len(self.list)):
				if supstr(word, self.list[i]):
					self.list.insert(i, word)
					return
		self.list.append(word)
	
		
	def findPossible(self, possible, start, acc):
		for word in self.list:
			if isSubAnagram(possible, word):
				w=start+word
				if not (w in acc):
					acc.append(w)

import sys

from .dict import Dict
from .dictparser import DictParser
def nts(x):
	o=""
	for i in range(x-1): o+="  "
	return o

class IndexEntry:
	def __init__(self, depth=0, maxDepth=4):
		self.valid=False
		self.depth=depth
		self.maxDepth=maxDepth
		self.endWord=False
		self.children=[]
		if self.depth>=self.maxDepth: 
			self.children=IndexList()
			self.valid=True
	
	def fill(self):
		if self.depth<self.maxDepth:
			self.children=[]
			for i in Dict.ALPHABET:
				self.children.append(IndexEntry(self.depth+1, self.maxDepth))
			
	def ok(self):
		self.valid=True
		
	def __getitem__(self, itm):
		if type(itm)==str:
			return self.children[charToIndex(itm)]
		return self.children[itm]
	
	def __str__(self):
		x=""
		for i in range(len(self.children)):
			if self.children[i].valid:
				x+=indexToChar(i)
		return x
	
	def has(self, end):
		if self.depth<self.maxDepth:
			char=end[0]
			index=charToIndex(char)
			node=self.children[index]
			if not node.valid: return False
			if len(end)==1: return self.endWord
			return node.has(end[1:])
		else:
			return self.children.has(end[1:])
		
	def addWord(self, end, start=""):
		n=len(end)
		c=end[0] if n else ""
		nstart=c+start
		nend=end[1:] if len(end)>1 else ""
		
		
		if self.depth<self.maxDepth:
			if len(self.children)==0: self.fill()
			self.ok()
			if n==0: 
				self.endWord=True
				return 
			nex=charToIndex(c)
			
			self.children[nex].addWord(nend, nstart)
		else:
			self.children.addWord(end)

	
	def _findPossible(self, prefix, possible, acc=[]):
		if self.endWord and (not prefix in acc): acc.append(prefix)
		if self.depth<self.maxDepth:
			toDo=""
			for i in possible:
				if not (i in toDo): toDo+=i
			
			for i in toDo: #la lettre a verifier
				cc=self.children[charToIndex(i)]
				if cc.valid:
					cc._findPossible(prefix+i, possible.replace(i, '', 1), acc)
		else:
			self.children.findPossible(possible, prefix, acc)
		return acc
				
		
	def findPossible(self, possible):
		return self._findPossible("", possible)
		
	def __repr__(self):
		return str(self.__dict__)









def charToIndex(c):
	return Dict.ALPHABET.find(c)

def indexToChar(i):
	return Dict.ALPHABET[i]

class IndexedDict(Dict):
	def __init__(self, maxdepth=6, column=[[Dict.COLWORD, Dict.TYPESTRING]]):
		self.index=IndexEntry(0, maxdepth)
		Dict.__init__(self, column)

	def addWord(self, word):
		x=Dict.addWord(self, word)
		if x:
			self.index.addWord(word[self.wordCol])
		return x
	
	def findAll(self, prefix):
		return self.index.findAll(prefix)
		
	def findPossible(self, path):
		return self.index.findPossible(path)
		
	
	def __repr__(self):
		return str(self.__dict__)
	

