#!/usr/bin/python3


from wordgen import matrix
from dictionaire import indexeddict, dict, dictfeeder, dictparser

import time
import random

debug=False
toTest=[matrix.Word3Matrix, matrix.WordNMatrix]

#l = lexer.Lexer(reader.FileReader("dictionaire"))
if debug: print("Loading dictionaire")

ts0 = time.time()
path="data/livre"
#di=dictionaire.Dict(path)
#di=indexeddict.IndexedDict(path)
di=dictparser.DictParser.fromFile(path)

print("Dict time: "+str(time.time()-ts0)+" s\n")

l = dict.DictReader(di)

dfs = []
words=[]
scores=[]
for matrice in toTest:
	if debug: print("Loading "+matrice.__name__)
	dfs.append(dictfeeder.DictFeeder(l, matrice))
	words.append([])
	dfs[-1].load()
	l.reset()

if debug: print("Benchark")

ts = time.time()
for j in range(len(toTest)):
	total=100000
	n=0
	for i in range(total):
		df=dfs[j]
		word=df.mat.randWord(random.randint(4,10))
		words[j].append(( word, l.has(word)))
		n+= 1 if l.has(word) else 0
	scores.append(100.0*n/total)
	if debug: print(toTest[j].__name__+" : "+str( 100.0*n/total))
	
print("Find time: "+str(time.time()-ts)+" s")
print("Total time: "+str(time.time()-ts0)+" s")

col=""
for i in range(len(toTest)):
	col+=toTest[j].__name__+";Existe;"
print(col)

col=""
for j in range(len(toTest)):
	col+="score;"+("%.2f" % scores[j])+"%;"
print(col)

for i in range(total):
	col=""
	for j in range(len(toTest)):
		if j<len(words[j]):
			col+=words[j][i][0]+";"
			col+= "Oui;" if words[j][i][1] else "Non;"
		else:
			col+=";;"
	#print(col)



