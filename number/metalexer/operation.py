
class Node:

    def __init__(self):
        self.nexts={}
        self.prevs={}
        self.id=""+str(Node.maxId)
        Node.maxId+=1

    def assign(self, node):
        for char in node.nexts:
            self.connect(char, node.nexts[char])


    def endNodes(self, out=[]):
        for key in self.nexts:
            x=self.nexts[key]
            if x.node.isEnd():
                out.append(x)
            else:
                x.node.endNodes(out)
        return out

    def connect(self, char, node=None):
        if(node==None): node=Node()
        if not (char in self.nexts):
            x=node
            if type(x)!=NodePointer:
                x=NodePointer(node)
            self.nexts[char]=x
            x.node.prevs[char]=self
            return x

        raise Exception("Error")

    def next(self, c):
        if "-1" in self.nexts:
            return self.nexts["-1"]
        if (c in self.nexts):
            return self.nexts[c]

    def __repr__(self): return self.__str__()
    def __str__(self):
        return ""+str(self.id)


    def toDot(self):
        str=""

        for x in self.nexts:
            node=self.nexts[x]
            if x=="-1": x="*"
            else: x="'"+x+"'"
            str+=self.id+ " -> "+node.node.id+ " [label=\""+x+"\"];\n"+node.node.toDot()
        return str

    def isEnd(self): return len(self.nexts)==0



Node.maxId=0


class NodePointer:
    def __init__(self, node):
        self.node=node

    def __repr__(self): return self.__str__()

    def __str__(self): return str(self.node)

class Graph:
    def __init__(self):
        self.root=NodePointer(Node())
        self.end=self.root

    def setRoot(self, root):
        self.root=root

    def execStrict(self, string):
        return self.exec(string)==string

    def exec(self, string):
        i=0
        curr=self.root
        while curr!=None and not curr.node.isEnd():
            curr=curr.node.next(string[i])
            if curr!=None:
                i+=1
                if curr.node.isEnd(): return string[:i]
                if i>=len(string): return None
            else: return None


    def toDot(self):
        return self.root.node.toDot()

    def exportDot(self):
        return "digraph G {\n"+self.toDot()+"\n}\n"

    def append(self, c, node=None):
        if node==None: node=Node()
        if c==None: c="-1"
        if type(node)==Graph:
            self.end.node.connect(c, node.root)
            self.end=node.end
        else:
            self.end = self.end.node.connect(c, node)
        return self.end

    def addOr(self, c, node=None):
        if node==None: node=Node()
        if type(c)==str:
            self.root.node.connect(c, node)
            for x in self.root.node.endNodes():
                x.node=self.end.node
        if type(c)==Graph:
            node=c
            self.root.node.assign(node.root.node)
            node.end.node=self.end.node
        return self.end




