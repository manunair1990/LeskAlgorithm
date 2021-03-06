import nltk
import math
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from collections import Counter

sent=raw_input("Enter the sentence: ")
wrd=raw_input("Enter the word to disambiguate: ")
#wrd<- the word to disambiguate
token=nltk.word_tokenize(sent)
token1=[w for w in token if not w in stopwords.words('english')] 

context=[]
for i in range(len(token1)):
	context.append(token1[i])

while wrd in context:
	context.remove(wrd)
#context<-list of context words

wrdsns=[]
wrddef=[]
wrddeftkn=[]
#wrdsns<- list of senses for 'wrd'
#wrddef<- list of definitions of each senses

for i in range(len(wn.synsets(wrd))):
	wrdsns.append(wn.synsets(wrd)[i])
	wrddef.append(wn.synsets(wrd)[i].definition)

for i in range(len(wrddef)):
	porter=nltk.PorterStemmer()
	wtkn=nltk.word_tokenize(wrddef[i])
	wrddeftkn.append([porter.stem(w) for w in wtkn if w.isalpha() and not w in stopwords.words('english') and w not in [wrd]])

#wrddeftkn<- list of tokenized words of 'wrddef'
contextdef=[]
con=[]
contkn=[]

#ccontextdef<- list of definitions of 'context' words
for i in context:
	for j in range(len(wn.synsets(i))):
		contextdef.append(wn.synsets(i)[j].definition)

for i in range(len(contextdef)):
	porter=nltk.PorterStemmer()
	con=nltk.word_tokenize(contextdef[i])
	contkn.append([porter.stem(w) for w in con if w.isalpha() and not w in stopwords.words('english') and w not in [wrd]])

#contkn<- list of tokenized words of 'ccontext'

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     #print intersection
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

bstsns=[]
maxovrlap=0
print context
for i in range(len(wrddeftkn)):
	for j in range(len(contkn)):
		ovrlap=get_cosine(Counter(wrddeftkn[i]),Counter(contkn[j]))
		if ovrlap>maxovrlap:
			maxovrlap=ovrlap
			print maxovrlap,
			bstsns=wrddef[i]
			print bstsns
			
print "The best sense is: \n"
if bstsns==[]:
	print "failed\n"
	print wrddef[1]
else:
	print bstsns
