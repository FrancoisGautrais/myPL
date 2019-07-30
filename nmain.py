#!/usr/bin/python3
import inspect
from number.context import Context
import sys
context=Context()

#context.exec("def add(a,b) = a+b")
#print(context.exec("add(4, 6)"))
ret=context.execSourceFile("test.code")
#print(ret[0], "->", ret[1])
#context.execSourceFile("test2.code")
while True:
    #context.stack.print()
    sys.stdout.write(">>> ")
    sys.stdout.flush()
    line=sys.stdin.readline()
    if(len(line[:-1])==0): exit(0)
    ret=context.exec(line)
    print(ret[0], "->", ret[1])



"""
def a(x,y=1): return 0
def b(x,y=1, z=2): return 0
def c(x,y): return 0

class FunctionWrapper:
    def __init__(self, fct):
        self.ref=fct
        self.name=fct.__name__
        params=inspect.signature(fct).parameters

        self.nParamMin=0
        self.nParamMax=0
        self.nParam=len(params)
        for i in params:
            p=params[i]
            if p.default==inspect._empty:
                self.nParamMin+=1
            else: self.nParamMax+=1

    def __str__(self):
        return self.name+"("+str(self.nParam)+")["+str(self.nParamMin)+"-"+str(self.nParamMax)+"]"


print(FunctionWrapper(a))
print(FunctionWrapper(b))
print(FunctionWrapper(c))
print(FunctionWrapper(print))"""