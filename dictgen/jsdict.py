#!/usr/bin/python3

import json
import time
import sys
import unidecode

"""
ts=time.time()
arr=json.load(open("outBis", "r"))
delta=time.time()-ts
ts=time.time()
sys.stderr.write(str(delta)+" s\n")

arrout=[]
for obj in arr:
	if "fr" in obj["lang"]:
		for i in range(len(obj["lang"]["fr"])):
			obj["lang"]["fr"][i]=obj["lang"]["fr"][i].rstrip().lstrip().lower()
			
		arrout.append(obj)
print(json.dumps(arrout))
delta=time.time()-ts
sys.stderr.write(str(delta)+" s\n")




ts=time.time()
arr=json.load(open("dictfr.json", "r"))
delta=time.time()-ts
ts=time.time()
sys.stderr.write(str(delta)+" s\n")

natures=[]
for obj in arr:
	if "fr" in obj["lang"]:
		for n in obj["lang"]["fr"]:
			if not (n in natures):
				print(n)
				natures.append(n)
delta=time.time()-ts
sys.stderr.write(str(delta)+" s\n")
"""



"""

arr=json.load(open("dictfr.json", "r"))
out=[]
for obj in arr:
	if "nom" in obj["lang"]["fr"]:
		out.append(obj["mot"])
		
out=sorted(out)
for i in out:
	print(i)
"""
alphabet=["aàáâãäåæ", "b", "cç", "d", "eèéêë", "f", "g", "h", "iìíîï", "j", "k", "l", 
		"m", "nñ", "oòóôõöøù", "p", "q", "r", "s", "t", "uúûü", "v", "w", "x", "yýÿ", "z"]

def isValid(s):
	for c in s:
		ok=False
		for i in alphabet:
			if c in i: 
				ok=True
				break
		if not ok: return False
	return True

def charToIndex(c):
	for i in range(len(alphabet)):
		if c in alphabet[i]:
			return i
	return -1

def compare(a):
	return unidecode.unidecode(a.lower())

arr=json.load(open("dictfr.json", "r"))
dictionaire=[]
for word in arr:
	ok=True
	if isValid(word["mot"].lower()):
		dictionaire.append(word["mot"])

s=""
for i in sorted(dictionaire, key=compare):
	print(i)



