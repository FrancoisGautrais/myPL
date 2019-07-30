#!/usr/bin/python3
import sys
from pympler.asizeof import asizeof
from dict.dict import Dict
from wordgen.matrixloader import MatrixLoader
from dict.indexeddict import IndexedDict
from dict.anagrammaker import AnagramMaker
from dict.dictparser import Parser
import time
import random

"""
#d=Parser.fromTextFile("data/dict/fr.courrant.dict", IndexedDict())
#d=Parser.fromTextFile("data/dict/fr.courrant.dict", IndexedDict(3))
d=Parser.fromTextFile("data/livre", Dict())
d1=Parser.fromTextFile("data/livre", IndexedDict(3))


mat=MatrixLoader.matrixFromDict(d)
words=[]
for i in range(1000):
	words.append(mat.randWord(random.randint(4,18)))

test = [d,d1]

for i in range(2):
	for dico in test:
		t0=time.time()
		for w in words:
			dico.has(w)
		print("Execution time for "+type(dico).__name__+" : ", "%.3f" % (time.time()-t0))
	



"""
show=False
times=[]
lt=time.time()
d=Parser.fromDictFile("data/dict/fr.courrant.dict", Dict())
times.append(time.time()-lt)

lt=time.time()
d1=Parser.fromTextFile("data/dict/fr.courrant.dict", IndexedDict(6))
times.append(time.time()-lt)
test=[d, d1]

mat=MatrixLoader.matrixFromDict(d)
words=[]
NGEN=[1, 10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10, 50, 100, 200]

print("start")
for N in NGEN:
	print("=====", N, " générations =====")
	words=[]
	for i in range(N):
		words.append(mat.randWord(random.randint(4,18)))
		
	for i in range(len(test)):
		dico=test[i]
		print("\t=====", type(dico).__name__, "=====")
		t=time.time()
		an=AnagramMaker(dico)
		for w in words:
			ws=an.generateFromString(w)
		execTime=time.time()-t
		print("\tExec time = ", "%.3f" % execTime, " Per item=", "%.6f" % (execTime/float(N)))
	print("")
	
	
	
"""
di = IndexedDict()
di.addWord(["beau"])
di.addWord(["belle"])
di.addWord(["belles"])
di.addWord(["belless"])
di.addWord(["bellesa"])
di.addWord(["belleaa"])
di.addWord(["belleab"])
print(di.has("beau"))
print(di.has("belles"))
print(di.has("bellesd"))
"""
