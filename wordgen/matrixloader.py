#!/usr/bin/python3
import sys
sys.path.insert(0,'..')

from .matrix import Word3Matrix
from dictionaire.dict import DictReader

class MatrixLoader:
	def __init__(self, reader, matClass=Word3Matrix, ponderate=True):
		self.mat=matClass()
		self.ponderate=ponderate
		self.reader=reader
		if self.mat==None:
			self.mat=matrix.WordMatrix()
		
	def load(self):
		while self.reader.hasNext(): 
			x=self.reader.next()
			if self.ponderate:
				self.mat.addWord(*x)
			else:
				self.mat.addWord(x[0])
		return self
				
	@staticmethod
	def matrixFromDict(dico, matClass=Word3Matrix, ponderate=True):
		return MatrixLoader(DictReader(dico)).load().mat
