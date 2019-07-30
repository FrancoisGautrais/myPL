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
		parser=Parser(StringIOWrapper(string))
		res=parser.parse()
		return (res, res.eval(self.stack))

	def execSourceFile(self, path):
		fd=open(path, "r")
		txt=fd.read()
		ret=self.exec(txt)
		fd.close()
		return ret