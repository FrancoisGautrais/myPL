#!/usr/bin/python3

from number.context import Context
import sys
context=Context()

#context.exec("def add(a,b) = a+b")
#print(context.exec("add(4, 6)"))
context.execSourceFile("test.code")
#context.execSourceFile("test2.code")
while True:
    context.stack.print()
    sys.stdout.write(">>> ")
    sys.stdout.flush()
    line=sys.stdin.readline()
    if(len(line[:-1])==0): exit(0)
    ret=context.exec(line)
    print(ret[0], "->", ret[1])


