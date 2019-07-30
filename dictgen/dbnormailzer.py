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

def normalize(x):
	xx=x.rstrip().lstrip().lower()
	for key in natureMat:
		if xx in natureMat[key]:
			return key
	return "inconnu"

arr=json.load(open("outBis.fr", "r"))

premier=1
for obj in arr:
	if "fr" in obj["lang"]:
		for i in range(len(obj["lang"]["fr"])):
			obj["lang"]["fr"][i]=normalize(obj["lang"]["fr"][i])
		print( ("[" if premier else ",")+json.dumps(obj))
		premier=0
print("]")

