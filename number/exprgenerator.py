#!/usr/bin/python3

from math import log, exp
from .operation import *
from  random import randint

def randNumber(min, max):
	return randint(min, max)
	

def randLogNumber(min, max):
	base=1.1
	return max-int(log(randint(int(base**(min)), int(base**(max))))/log(base))

class ExprSet:
	def __init__(self):
		self.numbers=[]
		self.resultInt=0
		self.result=None

class ExprGeneratorParam:
	def __init__(self):
		self.countMaxNumber=7
		self.countMinNumber=5
		self.cbCountNumber=randNumber
		
		self.countMaxOp=7
		self.countMinOp=5
		self.cbCountOp=randNumber
		
		self.valMaxNumber=1000
		self.valMinNumber=1
		self.cbValNumber=randLogNumber
		
		self.addWeight=10
		self.subWeight=2
		self.mulWeight=6

class ExprGenerator:
	def __init__(self, params=ExprGeneratorParam()):
		self.setParams(params)
		self.ops=[]
		
	def _addOp(self, op):
		self.ops.append(op)
		
	def _getRandOp(self):
		x=self.ops[randint(0, len(self.ops)-1)]
		self.ops.remove(x)
		return x
	
	def setParams(self, params):
		self.params=params
	
	def _genCountOp(self):
		return self.params.cbCountOp(self.params.countMinOp,self.params.countMaxOp)
	
	def _genCount(self):
		return self.params.cbCountNumber(self.params.countMinNumber,self.params.countMaxNumber)
		
	def _genVal(self):
		return self.params.cbValNumber(self.params.valMinNumber ,self.params.valMaxNumber)
	
	def _genOp(self, a, b):
		total=self.params.addWeight+self.params.subWeight+self.params.mulWeight
		x=randint(0,total)
		if x<self.params.addWeight: return Addition(a,b)
		elif x<self.params.addWeight+self.params.subWeight: 
			return Soustraction(a,b) if a.eval()>b.eval() else Soustraction(b, a)
		return Multiplication(a,b)
	
	def _findLongerOp(self):
		max=0
		opmax=None
		for op in self.ops:
			x=op.countAll()
			if x>max:
				max=x
				opmax=op
		return opmax
				
	
	def generate(self):
		count=self._genCount()
		self.ops=[]
		ret=ExprSet()
		
		for i in range(count):
			val=self._genVal()
			self._addOp(Number(val))
			ret.numbers.append(val)
			
		for i in range(self._genCountOp()):
			a=self._getRandOp()
			if len(self.ops)==0: 
				ret.result=a
				ret.resultInt=a.eval()
				return ret
				
			b=self._getRandOp()
			
			if len(self.ops)==0: 
				result= a if a.countAll()>b.countAll() else b
				ret.result=result
				ret.resultInt=result.eval()
				return ret
				
			self._addOp(self._genOp(a,b))
		ret.result=self._findLongerOp()
		ret.resultInt=ret.result.eval()
		return ret
		
		
			
