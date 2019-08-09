#!/usr/bin/python3
import sys
import unidecode


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

def compare(a):
	return unidecode.unidecode(a.lower())
	
class Dict:
	ALPHABET='abcdefghijklmnopqrstuvwxyzàâæçèéêëîïñôùûüœ'
	
	TYPEINT="int"
	TYPESTRING="str"
	TYPEFLOAT="float"
	COLWORD="word"
	COLCOUNT="count"
	COLNATURE="nature"
	
	
	def __init__(self, column=[["word", "str"]]):
		self.column=None
		self.wordCol=0
		self.countCol=-1
		self.natureCol=-1
		self.setColumn(column)
		
		self.dict={}
		self.freq={}
		self.freqTotal=0
		for i in Dict.ALPHABET:
			self.freq[i]=0
		self.total=0
	
	def setColumn(self, col):
		self.column=col
		for i in range(len(col)):
			if col[i][0]==Dict.COLCOUNT:
				self.countCol=i
			elif col[i][0]==Dict.COLWORD:
				self.wordCol=i
			elif col[i][0]==Dict.COLNATURE:
				self.natureCol=i
	
	def getWord(self, i):
		return self[i][self.wordCol]
	
	def getCount(self, i):
		return self[i][self.countCol] if self.countCol>0 else 1
		
	def getNature(self, i):
		return self[i][self.natureCol] if self.countCol>0 else "i"
	
	def __getitem__(self, i):
		if type(i)==int:
			return self.dict[list(self.dict.keys())[i]]
		elif type(i)==str:
			return self.dict[i]
		else:
			raise Exception("Dict::__getitem__ bad parameter expected int or str")
	
	def has(self, word):
		return word.lower() in self.dict
	
	def _addFreq(self, char, weight=1):
		if not (char in self.freq):
			self.freq[char]=0
		if self.countCol>=0: 
			self.freq[char]+=weight
			self.freqTotal+=weight
	
	def addWord(self, word):
		poids=word[self.countCol]
		if not (word[self.wordCol] in self.dict):
			self.dict[word[self.wordCol]]=word
			return True
		if self.countCol>=0: 
			self.dict[word[self.wordCol]][self.countCol]+=poids
		for c in word[self.wordCol]:
			self._addFreq(c, poids)
		return False

	def length(self):
		return len(self.dict)
				
	def keys(self):
		x=self.dict.keys()
		out=[]
		for i in x:
			out.append(i)
		return out
		
	def write(self, fd):
		s="#="
		for col in self.column:
			if len(s)>2: s+="|"
			s+=col[0]+":"+col[1]
		fd.write(s+"\n")
		for key in self.dict:
			word=self.dict[key]
			s=""
			for j in range(len(word)):
				if j>0: s+="|"
				s+=str(word[j])
			fd.write(s+"\n")
	
	def print(self):
		self.write(sys.stdout)
		
	def printFreq(self):
		keys=[]
		for c in self.freq:
			keys.append(c)
		sortedKeys=sorted(keys, key=compare)
		den=float(self.freqTotal)/100 if self.freqTotal>0 else 1
		for k in sortedKeys:
			print(k+":"+( "%.2f" % (float(self.freq[k]) / den ) ))
	
	def findPossible(self, possible):
		acc=[]
		for word in self.dict.keys():
			if isSubAnagram(possible, word):
				acc.append(word)
		return acc
		
		

class DictReader:
	def __init__(self, d):
		self.dict=d
		self.keys=d.keys()
		self.index=-1
		self.len=len(self.keys)
	
	def reset(self):
		self.index=-1
	
	def hasNext(self):
		return self.index+1<self.len
		
	def next(self):
		self.index+=1
		if self.index>=self.len:
			raise Exception("DictReader out of bound")
		return self.peek()
	
	def peek(self):
		k=self.keys[self.index]
		return ( self.dict.getWord(k), self.dict.getCount(k))
		
	def has(self, word):
		return self.dict.has(word)
		
		


#d.print()
#for i in d.freq:
#	print(i+";"+("%.3f" % (float(d.freq[i])/d.total*100)).replace(".", ","))

#print(sorted(d.list))

