
class Node:
    def __init__(self):
        self.nexts=[]
        self.parent=None

    def addNext(self, next):
        self.nexts.append(next)

    def __repr__(self): return self.__str__()

    def __str__(self):
        raise NotImplementedError("")

    def has(self, char):
        raise NotImplementedError("")

    def setParent(self, parent):
        self.parent=parent
        return self

    def addNextToEnd(self, node):
        if len(self.nexts)==0:
            return self.addNext(node)
        for n in self.nexts:
            n.addNextToEnd(node)

    def _exec(self, end, acc):
        n=self.has(end)
        if n==None: return None
        acc+=end[:n]
        end=end[n:]
        if len(end)==0 or len(self.nexts)==0: return acc

        max=0
        retMax=None
        for node in self.nexts:
            ret=node._exec(end, acc)
            if ret!=None:
                count=len(ret)
                if count>max:
                    max=count
                    retMax=ret
        return retMax

    def exec(self, string):
        return  self._exec(string, "")


    def _str_after(self):
        after=""
        if len(self.nexts)>1:
            after="("
            for i in range(len(self.nexts)):
                if i>0: after+="|"
                after+=str(self.nexts[i])
            after+=")"
        elif len(self.nexts)==1: after=str(self.nexts[0])
        else: after=";" if self.parent==None else ""
        return after

class Container(Node):
    def __init__(self, start=None):
        Node.__init__(self)
        self.start=start

    def setStart(self, start):
        self.start=Parentheses(start)
        start.setParent(self)
        return self


class Parentheses(Container):
    def __init__(self, start):
        Container.__init__(self)
        self.start=start


    def has(self, end):
        n = self.start.exec(end)
        if n == None: return None
        return len(n)

    def __str__(self):
        return "(" + str(self.start) + ")"

class FacultativeSelector(Container):
    def __init__(self):
        Container.__init__(self)

    def has(self, end):
        n = self.start.has(end)
        if n == None: return 0
        return n

    def __str__(self):
        return "(" + str(self.start) + ")?" + self._str_after()


class PlusSelector(Container):
    def __init__(self):
        Container.__init__(self)

    def has(self, end):
        acc = self.start.has(end)
        if acc==None: return None
        n=0
        while n!=None:
            n=self.start.has(end[acc:])
            if n!=None: acc+=n
        return acc

    def __str__(self):
        return "(" + str(self.start) + ")+" + self._str_after()


class StarSelector(Container):
    def __init__(self):
        Container.__init__(self)

    def has(self, end):
        acc=0
        n=0
        while n!=None:
            n=self.start.has(end[acc:])
            if n!=None: acc+=n
        return acc

    def __str__(self):
        return "(" + str(self.start) + ")*" + self._str_after()

class NumberSelector(Container):
    def __init__(self, n):
        Container.__init__(self)
        self.times=n

    def has(self, end):
        acc = 0
        n = 0
        i=0
        while n != None and i<self.times:
            n = self.start.has(end[acc:])
            if n != None: acc += n
            i+=1
        return acc if i==self.times and n!=None else None

    def __str__(self):
        return "(" + str(self.start) + "){"+str(self.times)+"}" + self._str_after()

class NumberRangeSelector(Container):
    def __init__(self, min, max):
        Container.__init__(self)
        self.min=min
        self.max=max

    def has(self, end):
        acc = 0
        n = 0
        i=0
        while n != None and i<self.max:
            n = self.start.has(end[acc:])
            if n != None:
                acc += n
                i+=1
        return acc if i>=self.min or n!=None else None

    def __str__(self):
        return "(" + str(self.start) + "){"+str(self.min)+","+str(self.max) +"}"+ self._str_after()


class Alternation(Node):
    def __init__(self):
        Node.__init__(self)
        self.possible=[]

    def addPossibility(self, p):
        self.possible.append(p)

    def has(self, end):
        max=0
        ok=False
        for node in self.possible:
            n=node.has(end)
            if n!=None:
                ok=True
                if n>max: max=n
        return max if ok else None

    def __str__(self):
        x="("
        for i in range(len(self.possible)):
            if i>0: x+="|"
            x+=str(self.possible[i])
        return x+")"+self._str_after()
"""
class String(Container):
    def __init__(self, string):
        Node.__init__(self)

        if len(string)>0:
            curr=Char(string[0])
            self.nexts.append(curr)
            for i in range(1, len(string)):
                tmp=Char(string[i])
                curr.addNext(tmp)
                curr=tmp
            self.end=curr

    def addNext(self, next):
        self.end.addNext(next)

    def has(self):
        if len(self.nexts)>0: return self.nexts[0].test()
        return False

    def __str__(self):
        if len(self.nexts)>0: return str(self.nexts[0])
"""

class Char(Node):
    def __init__(self, chars):
        Node.__init__(self)
        self.chars=chars

    def has(self, c):

        return 1 if c[0] in self.chars else None

    def isAlfaNum(self):
        return self.chars.isalnum()

    def __str__(self):
        if len(self.chars)==1: return self.chars[0]+self._str_after()
        return self.chars+self._str_after()

class Dot(Node):
    def __init__(self):
        Node.__init__(self)

    def has(self, c):
        return 1

    def __str__(self):
        return "."+self._str_after()

class Range(Node):
    def __init__(self, first, second):
        Node.__init__(self)
        self.first=first.chars[0]
        self.second=second.chars[0]

    def has(self, char):
        min=self.first if self.first<self.second else self.second
        max=self.first if self.first>self.second else self.second
        return 1 if char>=min and char<=max else None

    def __str__(self):
        return self.first+"-"+self.second+self._str_after()


class Class(Node):
    def __init__(self):
        Node.__init__(self)
        self.ranges=[]

    def addRange(self, range):
        self.ranges.append(range)

    def has(self, char):
        for range in self.ranges:
            if range.has(char) : return 1
        return None

    def __str__(self):
        x="["
        for range in self.ranges: x+=str(range)
        return  x+"]"+self._str_after()