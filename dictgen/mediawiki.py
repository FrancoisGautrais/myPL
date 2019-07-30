#!/usr/bin/python3
import json
import xml.etree.ElementTree as ET
import sys

class MWReader:
	def __init__(self, text):
		self.text=text.split("\n")
		self.index=-1
		self.len=len(self.text)
		self.line=""
		
	
	def readline(self):
		self.index+=1
		if self.index>=self.len: return ""
		self.line=self.text[self.index]+"\n"
		return self.line

def nToSpace(n):
	x=""
	for i in range(n):
		x+="  "
	return x

class MWNode:
	ROOT=0
	TITLE1=1
	TITLE2=2
	TITLE3=3
	TITLE4=4
	TITLE5=5
	TITLE6=6
	
	def __init__(self, parent, ty, tag):
		self.parent=parent
		self.title=tag
		self.type=ty
		self.children=[]
		self.text=[]
		
	def appendText(self, txt):
		self.text.append(txt)
		
	def add(self, x):
		self.children.append(x)
		
	def print(self, n=0):
		space=nToSpace(n)
		print(space+str(self.title))
		for i in self.text:
			print(space+"  "+i[:-1])
		for i in self.children:
			i.print(n+1)
		

class MWParser:
	def __init__(self, text):
		self.reader=MWReader(text)
		self.root=MWNode(None, 0, "")
	
	def _parseTitle(self, line):
		i=0
		n=0
		titre=""
		while i<len(line) and  line[i]=="=":
			i=i+1
		i+=1
		n=i
		while i+1<len(line) and line[i]!="=":
			i+=1
			titre+=line[i]
		titre=titre[1:-4]
		return (n, titre.split("|"))
	
	def parse(self):
		current=self.root
		#print(self.reader.text)
		line=self.reader.readline()
		while line!="":
			if line[0]=="=":
				n, titre = self._parseTitle(line)
				while current.type>=n: 
					current=current.parent
				md=MWNode(current, n, titre)
				current.add(md)
				current=md
			else:
				current.appendText(line[:-1])
			line=self.reader.readline()
		return self.root



class MWPage:
	
	def __init__(self, elem):
		txt=""
		self.mot=""
		textNode=elem.find('{http://www.mediawiki.org/xml/export-0.10/}revision/{http://www.mediawiki.org/xml/export-0.10/}text')
		titleNode=elem.find('{http://www.mediawiki.org/xml/export-0.10/}title')
		if textNode!=None:
			txt=ET.tostring(textNode, encoding="utf8", method="text").decode("utf8")
			self.mot=ET.tostring(titleNode, encoding="utf8", method="text").decode("utf8").split("\n")[0]
		parser=MWParser(txt)
		self.root=parser.parse()
		
		self.langues={}
		for child in self.root.children:
			t=child.title
			if len(t)>=2 and t[0]=="langue":
				lan=t[1]
				obj=[]
				for itm in child.children:
					d=itm.title
					if len(d)>=3 and d[0]=="S" and d[2]==lan:
						obj.append(d[1])
				self.langues[lan]=obj
	
	def toJson(self):
		tmp={}
		tmp["mot"]=self.mot
		tmp["lang"]=self.langues
		return json.dumps(tmp)
	
	def print(self):
		print(self.langues)
	
	def has(self, nature, lang="fr"):
		if lang in self.langues:
			return nature in self.langues[lang]
		return False
"""
fd = open("page2.wiki", "r")

if True:
	mw = MWPage(MDReader(fd.read()))
	#mw = MWPage(fd)
	mw.print()
	print(mw.toJson())
	fd.close()

x=MDReader(fd.read())
while x.readline()!="":
	print(x.line)
				
"""
