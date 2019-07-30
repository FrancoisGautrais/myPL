#!/usr/bin/python3
import random

class CharVector:
	def __init__(self):
		self.vect={}
		self.total=0.0
		
	def __getitem__(self, x):
		if (not (x in self.vect)) or self.total==0: return 0
		return float(self.vect[x])/self.total
	
	def randChar(self, end=False):
		#if end:
		#	if self[' '] and self[' ']>0:
		#		return ' '
		#	return None
		x=random.random()
		for i in self.vect:
			x-=self[i]
			if x<0 and self[i]!=' ':
				return i
		return ' '
		
	def addSequence(self, to, weight=1):
		if not (to in self.vect):
			self.vect[to]=0
		self.vect[to]+=weight
		self.total+=weight
		
	def getTotal(self):
		return self.total
		
	def print(self, alphabet, prefix=""):
		s=prefix
		for i in alphabet:
			if i in self.vect:
				s+="%.2f" % (self[i]*100)
			s+=";"
		print(s)

class CharMatrix:
	def __init__(self):
		self.mat={}
	
	def addSequence(self, fr, to, weight=1):
		if not (fr in self.mat):
			self.mat[fr]=CharVector()
		self.mat[fr].addSequence(to, weight)
	
	def __getitem__(self, x):
		if not (x in self.mat): 
			self.mat[x]=CharVector()
		return self.mat[x]
		
	def randChar(self, fr, end=False):
		return self[fr].randChar(end)
	
	def print(self, alphabet):
		col=";"
		for i in alphabet: col+=i+";"
		print(col)
		for i in alphabet:
			if i in self.mat:
				self.mat[i].print(alphabet, i+";")
			else:
				print(i+";")
	
class AbsWordMatrix:
	def __init__(self):
		self.alphabet=[]
		
	def addWord(self, word, weight=1):
		raise NotImplementedError()
		
	def addWord(self, word, weight=1):
		raise NotImplementedError()
		
	def randWord(self, size=6):
		raise NotImplementedError()
	
	def print(self):
		raise NotImplementedError()
		
	

class Word3Matrix(AbsWordMatrix):
	def __init__(self):
		AbsWordMatrix.__init__(self)
		self.mats=[]
	
	def addWord(self, word, weight=1):
		self._addSequence(' ', word[0], 0, weight)
		for i in range(0, len(word)-1):
			self._addSequence(word[i], word[i+1], 1, weight)
		self._addSequence(word[len(word)-1], ' ', 2, weight)
	
	def _addSequence(self, fr, to, index, weight):
		if not (fr.lower() in self.alphabet): 
			self.alphabet.append(fr.lower())
			self.alphabet=sorted(self.alphabet)
		
		
		while index>=len(self.mats):
			self.mats.append(CharMatrix())
		self.mats[index].addSequence(fr, to, weight)
	
	def randWord(self, size=6):
		word=self.mats[0].randChar(' ')
		i=0
		while i<size-1:
			n= 1 if i<size else 2
			c=self.mats[n].randChar(word[-1])
			if c==' ': return word
			if c!=None:
				word+=c
				i+=1
		return word
		
	
	def print(self):
		for i in range(len(self.mats)):
			print("step;"+str(i))
			self.mats[i].print(self.alphabet)
			print("")
			print("")
			
		

class WordNMatrix(AbsWordMatrix):
	def __init__(self):
		AbsWordMatrix.__init__(self)
		self.mats=[]
	
	def addWord(self, word, weight=1):
		self._addSequence(' ', word[0], 0, weight)
		for i in range(0, len(word)-1):
			self._addSequence(word[i], word[i+1], i+1, weight)
		self._addSequence(word[len(word)-1], ' ', len(word)+1, weight)
	
	def _addSequence(self, fr, to, index, weight):
		if not (fr.lower() in self.alphabet): 
			self.alphabet.append(fr.lower())
			self.alphabet=sorted(self.alphabet)
		while index>=len(self.mats):
			self.mats.append(CharMatrix())
		self.mats[index].addSequence(fr, to, weight)
	
	def randWord(self, size=6):
		if size>=len(self.mats)+1:
			raise Exception("La taille de la matrice n'est pas suffisante : "+str(size)+">="+str(len(self.mats)+1))
		word=self.mats[0].randChar(' ')
		i=0
		while i<size-1:
			c=self.mats[i+1].randChar(word[-1])
			if c==' ': return word
			if c!=None:
				word+=c
				i+=1
		return word
		
	
	def print(self):
		for i in range(len(self.mats)):
			print("step;"+str(i))
			self.mats[i].print(self.alphabet)
			print("")
			print("")
		

