#!/usr/bin/python3
import sys
xmlpath="/home/ptitcois/src/frwiktionary-20190720-pages-articles-multistream.xml"
import time
import xml.etree.cElementTree as etree
import xml.etree.ElementTree as ET
from mediawiki import MWPage

deep=-1
def nToSpace(n):
	x=""
	for i in range(n):
		x+="  "
	return x

count=0
ncount=0
ts=time.time()
ts0=time.time()
ntotal=3765
for event, element in etree.iterparse(xmlpath, events=("start", "end")):
	if event=="start": 
		#print(nToSpace(deep)+element.tag.replace("{http://www.mediawiki.org/xml/export-0.10/}",""))
		deep+=1
	else: 
		deep-=1
	tag=element.tag.replace("{http://www.mediawiki.org/xml/export-0.10/}","")

	if event=="end" and tag=="page":
		mw = MWPage(element)
		print(("," if (count or ncount) else "[")+str(mw.toJson()))
		element.clear()
		
		ncount+=1
		if ncount>1000:
			ncount=0
			count+=1
			delta=time.time()-ts
			delta0=time.time()-ts0
			ts=time.time()
			#sys.stderr.write(str(count)+" : "+str(int(1000/delta))+" /s total: "+str(int(1000*count/delta0))+" /s\n")
			nPerS=1000*count/delta0
			left=ntotal-count
			t=int(left*1000/nPerS)
			sys.stderr.write(str(count)+" Restant: "+ str(int(t/60))+" m "+str(t%60)+" s  moyenne: "+str(int(1000*count/delta0))+" s\n")
			
print("]")

