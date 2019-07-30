#!/usr/bin/python3
from .parser import Parser
from .lexer import StringIOWrapper
from .operation import Stack

class Context:
	
	def __init__(self):
		self.stack=Stack()
		self.stack.set("__stack__", self.stack)
		self.stack.set("__context__", self)

	def exec(self, string):
		res=self.parse(string)
		return (res, res.eval(self.stack))


	def parse(self, string):
		parser=Parser(StringIOWrapper(string))
		res=parser.parse(self)
		return res


	def execSourceFile(self, path):
		fd = open(path, "r")
		txt = fd.read()
		ret = self.exec(txt)
		fd.close()
		return ret

	def parseSourceFile(self, path):
		fd=open(path, "r")
		txt=fd.read()
		ret=self.parse(txt)
		fd.close()
		return ret