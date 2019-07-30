#!/usr/bin/python3
import json
import time
import sys

natureMat = {
	"verbe":["verbe"],
	"pronom":["pronom","pronom démonstratif","pronom indéfini","pronom interrogatif","pronom personnel","pronom possessif","pronom relatif"],
	"préposition":["préposition","prép"],
	"onomatopée":["onomatopée","onom"],
	"nom propre":["nom propre","nom-pr","nom de famille","nom scientifique","nom-fam","patronyme","prénom"],
	"nom":["nom","nom commun","substantif"],
	"locution":["locution","locution phrase","locution-phrase"],
	"interjection":["interjection","interj"],
	"conjonction":["conjonction de coordination","conjonction"],
	"article":["article partitif","article indéfini","article défini/indéfini/partitif","article défini"],
	"adverbe":["adverbe","adv","adverbe interrogatif","adverbe relatif"],
	"adjectif":["adjectif","adj","adjectif démonstratif","adj-dém","adjectif exclamatif","adjectif indéfini","adjectif interrogatif","adjectif numéral","adjectif possessif","adjectif relatif"]
}

natToLetter =  { "verbe" : "v", 
								"pronom": "P", 
								"préposition": "p", 
								"onomatopée" : "o", 
								"nom propre" : "N", 
								"nom" : "n", 
								"locution" : "l", 
								"interjection" : "i", 
								"conjonction" : "c", 
								"article" : "r", 
								"adverbe" : "A", 
								"adjectif" : "a",
								"inconnu": "i"
							}
letterToMat = {
							  "v" : "verbe",  
								"P":"pronom",
								"p":"préposition", 
								"o":"onomatopée",  
								"N":"nom propre",  
								"n":"nom",  
								"l":"locution",  
								"i":"interjection",  
								"c":"conjonction",  
								"r":"article",  
								"A":"adverbe",  
								"a":"adjectif",
								"i": "inconnu"
							}

def normalize(x):
	xx=x.rstrip().lstrip().lower()
	for key in natureMat:
		if xx in natureMat[key]:
			return key
	return "inconnu"
	
def longNatToLetters(natures):
	out=""
	for nat in natures:
		if nat in natToLetter:
			if not natToLetter[nat] in out:
				out+=natToLetter[nat]
	if len(out)==0:
		out="i"
	return out

arr=json.load(open("data/outBis.fr", "r"))

exclude=": "
filter="vPpoNnlicrAai"
if len(sys.argv)>1: filter=sys.argv[1]

for obj in arr:
	if "fr" in obj["lang"]:
		mot=obj["mot"]
		ok=True
		for i in mot:
			if i in exclude:
				ok=False
				break
				
		for i in range(len(obj["lang"]["fr"])):
			obj["lang"]["fr"][i]=normalize(obj["lang"]["fr"][i])
		nats=longNatToLetters(obj["lang"]["fr"])
		for i in nats:
			if i in filter:
				if ok: print(mot+"|"+nats)
				break

