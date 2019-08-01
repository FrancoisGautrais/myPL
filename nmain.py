#!/usr/bin/python3
import subprocess
from number.metalexer.operation import *
from number.metalexer.parser import Regex
x = Regex.compile("abc")
print(x.exec("abc"))
print(x.exec("abbc"))

def show(root):
    fd=open("/home/ptitcois/tmp/graph/test.dot", "w")
    fd.write(root.exportDot())
    fd.close()
    image = open("test.jpg", "w")
    subprocess.run(["dot", "-Tjpg", "/home/ptitcois/tmp/graph/test.dot"], stdout=image)
    image.close()
    subprocess.run(["display", "test.jpg"])

show(x)
"""

r1 = Graph()
r1.append("s")
r1.append("t")
r1.append("r")


r2 = Graph()
r2.append("i")
r2.append("n")
r2.append("t")

r3 = Graph()
r3.append("d")
r3.append(None)

root = Graph()
root.append("a")
root.append("b")
root.append("c")
root.addOr(r1)
root.addOr(r2)
root.addOr(r3)
root.addOr("g")
fd=open("/home/ptitcois/tmp/graph/test.dot", "w")
fd.write(root.exportDot())
fd.close()
print(root.exec("abc"))
print(root.exec("g"))
print(root.exec("gh"))
print(root.execStrict("str"))
print(root.execStrict("stri"))
print(root.exec("int"))
print(root.exec("d"))
print(root.exec("di"))

image=open("test.jpg", "w")
subprocess.run(["dot", "-Tjpg", "/home/ptitcois/tmp/graph/test.dot"], stdout=image)
image.close()
subprocess.run(["display", "test.jpg"])
"""
"""
from number.metalexer.parser import Regex
from number.metalexer.lexer import StringIOWrapper
import sys

def testParentheses():
    print("testParentheses()")
    reg=Regex.compile("abc(...)ghi")
    print("  ",reg.exec("abcdefghi")=="abcdefghi")
    print("  ",reg.exec("abcdeghi")==None)
    print("  ",reg.exec("abcdddeghi")==None)

def testFacultativeSelector():
    print("testFacultativeSelector()")
    reg=Regex.compile("a[bd]?c")
    print("  ",reg.exec("abc")=="abc")
    print("  ",reg.exec("adc")=="adc")
    print("  ",reg.exec("abdc")==None)
    print("  ",reg.exec("ac")=="ac")
    print("  ",reg.exec("bc")==None)
    reg=Regex.compile("[bd]?c")
    print("  ",reg.exec("bc")=="bc")
    print("  ",reg.exec("dc")=="dc")
    print("  ",reg.exec("abdc")==None)
    print("  ",reg.exec("c")=="c")
    reg=Regex.compile("(bd)?c")
    print("  ",reg.exec("bdc")=="bdc")
    print("  ",reg.exec("dc")==None)
    print("  ",reg.exec("c")=="c")


def testStarSelector():
    print("testStarSelector()")
    reg=Regex.compile("a[bd]*c")
    print("  ",reg.exec("ac")=="ac")
    print("  ",reg.exec("abdbdbbbbbdc")=="abdbdbbbbbdc")
    print("  ",reg.exec("abcc")=="abc")
    print("  ",reg.exec("ac")=="ac")
    print("  ",reg.exec("bc")==None)

def testPlusSelector():
    print("testPlusSelector()")
    reg = Regex.compile("a[bd]+c")
    print("  ", reg.exec("ac") == None)
    print("  ", reg.exec("abdbdbbbbbdc") == "abdbdbbbbbdc")
    print("  ", reg.exec("abcc") == "abc")
    print("  ", reg.exec("bc") == None)


def testNSelector():
    print("testNSelector()")
    reg = Regex.compile("a[bd]{3}c")
    print("  ", reg.exec("abdc") == None)
    print("  ", reg.exec("abdbc") == "abdbc")
    print("  ", reg.exec("abcc") == None)
    print("  ", reg.exec("abdbdc") == None)
    print("  ", reg.exec("bc") == None)


def testNMSelector():
    print("testNMSelector()")
    reg = Regex.compile("a(bd){3,5}c")
    print("  ", reg.exec("abdc") == None)
    print("  ", reg.exec("abdbdbdc") == "abdbdbdc")
    print("  ", reg.exec("abdbdc") == "abdbdc")
    print("  ", reg.exec("abdbddc") == "abdbddc")
    print("  ", reg.exec("abcc") == None)
    print("  ", reg.exec("bc") == None)


reg = Regex.compile("a(bd){3,5}c")
print("  ", reg.exec("abdbdbdc") == "abdbdbdc")
exit(0)
testParentheses()
testFacultativeSelector()
testStarSelector()
testPlusSelector()
testNSelector()
testNMSelector()
"""