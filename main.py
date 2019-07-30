#!/usr/bin/python3
import sys

from number import operation
from number.lexer import Lexer, StringIOWrapper
from number.parser import Parser
from number.context import Context
from math import log, exp
from random import randint
from number.exprgenerator import ExprGenerator

expr="pi+4*6"

exp=ExprGenerator()
ctx=Context()
while True:
	op=exp.generate()
	print("Faire ",op.resultInt," avec ",op.numbers)
	found=False
	while not found:
		ret=sys.stdin.readline()
		if ret=="\n": break
		res=ctx.exec(ret[:-1])
		print(res[0]," = ", res[1])
		if res[1]==op.resultInt: break
	print(op.result, " = ", op.result.eval(env))
"""
lex=Lexer(StringIOWrapper(expr))
lex.next()
while lex.token!=Lexer.TOK_END:
	print(Lexer.tokstr(lex.token)+" : '"+str(lex.data)+"'")
	lex.next()
"""

"""
parser=Parser(StringIOWrapper(expr))
op=parser.parse()
print(op,"=",op.eval())
"""

"""
min=0
max=10
N=1000
base=1.45
x=[]
for i in range(N):
	v=max-int(log(randint(int(base**(min)), int(base**(max))))/log(base))
	print(v)
	x.append(v)
	
print("")
acc=0
for i in range(N):
	acc+=x[i]
print(acc/N)
"""
