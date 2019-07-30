#!/usr/bin/python3

def nts(n):
    s=""
    for i in range(n): s+="  "
    return s

class SymbolEntry:
    def __init__(self, depth=0):
        self.isWord=False
        self.children={}
        self.depth=depth

    def _ok(self):
        self.isWord=True

    def isOk(self):
        return self.isWord

    def insert(self, start, end):
        if len(end)==0:
            self._ok()
            return
        c=end[0]
        end=end[1:]
        start+=c

        if not c in self.children:
            self.children[c]=SymbolEntry(self.depth+1)

        self.children[c].insert(start, end)

    def has(self, start, end):
        if len(end)==0:
            return self.isWord
        c=end[0]
        end=end[1:]
        start+=c
        if not c in self.children: return False
        return self.children[c].has(start, end)


    def getNode(self, start, end):
        if len(end)==0:
            return self
        c=end[0]
        end=end[1:]
        start+=c
        if not c in self.children: return False
        return self.children[c].getNode(start, end)


    def __repr__(self): return self.__str__()

    def __str__(self):
        return "\n"+nts(self.depth)+"("+str(self.isWord)+":"+str(self.children)+")"


class SymbolLexer:

    def __init__(self, symboles):
        self.symbols=list(symboles)
        self.root=SymbolEntry()
        self._constructTable()


    def _constructTable(self):
        for s in self.symbols:
            self.root.insert("", s)

    def __repr__(self): return self.__str__()

    def __str__(self):
        return self.root.__str__()

    def has(self, s):
        return  self.root.has("", s)

    def getNode(self, s):
        return  self.root.getNode("", s)

    def readNext(self, c, fd):
        char=""
        while self.getNode(char+c) and c!="":
            char+=c
            c=fd.read(1)

        if(self.has(char)): return char
        return ""
"""
sl=SymbolLexer(["<", "<=", ">", ">=", "=", "==", "!=", "+", "++", "+="])

print(sl.getNode(""))
print(sl.has("<"))
print(sl.getNode("<="))
print(sl.has("<=="))
print(sl.has("=>"))
"""