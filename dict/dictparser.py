#!/usr/bin/python3
if __name__=="__main__":
	from dict import Dict
else:
	from .dict import Dict



class DictParser:
	
	def __init__(self, path):
		self.column=[[]]
		self.path=path
		self.fd=open(path, "r")
		self.index=0
		self.nline=0
	
	def _parseWord(self, line):
		arr=line.split("|")
		if len(arr)!=len(self.column):
			raise Exception("Line "+str(self.nline)+" bad format expected "+str(len(self.column))+" found "+str(len(arr)))
		for i in range(len(arr)):
			t=self.column[i][1]
			if t==Dict.TYPEINT:
				arr[i]=int(arr[i])
			elif t==Dict.TYPEFLOAT:
				arr[i]=float(arr[i])
		return arr
			
	
	def parse(self, d):
		line=self._readline()
		if self._parseMeta(line):
			line=self._readline()
		d.setColumn(self.column)
			
		while line:
			if line[0]!="#":
				word=self._parseWord(line)
				d.addWord(word)
			line=self._readline()
		self.fd.close()
		return d
	
	def _readline(self):
		line=self.fd.readline()
		self.nline+=1
		self.index+=len(line)
		if len(line)==0: return None
		return line[:-1]
	
	
	# #=COL1:TYPE|COL2:TYPE2
	def _parseMeta(self, line):
		if line==None: return False
		self.column=[]
		if len(line)>2 and line[0]=="#" and line[1]=="=":
			headers=line[2:].split("|")
			for head in headers:
				data=head.split(":")
				if len(data)==1:
					self.column.append([data[0], dict.dict.Dict.TYPESTRING])
				else:
					self.column.append(data)
			return True
		return False
		
	@staticmethod
	def fromFile(path, dictionaire=Dict()):
		dp=DictParser(path)
		return dp.parse(dictionaire)
			
class TextParser:
	ALPHABET='abcdefghijklmnopqrstuvwxyzàâæçèéêëîïñôùûüœ'
	
	def __init__(self, path):
		self.char=""
		self.word=""
		self.fd=open(path, "r")
		
	def _nc(self):
		self.char=self.fd.read(1)
		
	def _nextWord(self):
		self.word=""
		self._nc()
		while ( not (self.char in TextParser.ALPHABET)) and self.char!='':
			self._nc()
		while (self.char.lower() in TextParser.ALPHABET) and self.char!='':
			self.word+=self.char
			self._nc()
		return self.word
		
	def parse(self, d):
		self._nextWord()
		d.setColumn([[Dict.COLCOUNT, Dict.TYPEINT],[Dict.COLWORD, Dict.TYPESTRING]])
		while self.word!="":
			d.addWord([1,self.word])
			self._nextWord()
		return d

class Parser:
	@staticmethod
	def fromDictFile(path, dictionaire=Dict()):
		dp=DictParser(path)
		return dp.parse(dictionaire)
	
	@staticmethod
	def fromTextFile(path, dictionaire=Dict()):
		dp=TextParser(path)
		return dp.parse(dictionaire)
		

if __name__=="__main__":
	path="data/livre"
	tp=TextParser(path)
	d=tp.parse(Dict())
			
		
