from gensim.models import KeyedVectors
from gensim import matutils
import numpy as np
import os.path
import sys

def loadmodel():
	return KeyedVectors.load_word2vec_format(os.path.join(os.path.dirname(__file__),os.pardir,'GoogleNews-vectors-negative300.bin'),binary=True)

def getstopwords():
	with open('stopwords.txt','r') as f:
		return frozenset(x[:-1] for x in f)

def getsentimentvectors(model):
	sentimentvectors = {}
	with open('sentiment_vectors.tsv','r') as f:
		for line in f:
			head,*tail = [cell for cell in line.split('\t')[:-1] if cell]
			words,weights = [],[]
			for y in tail:
				word,*weight = y.split(' ')
				if not model.__contains__(word):
					raise Exception(f"{word} is not in model")
				words.append(word)
				weights.append(float(weight[0]) if weight else 1.0)
			sentimentvectors[head] = KeyedVectors.get_mean_vector(model,words,np.array(weights),True,True,False)
	return sentimentvectors

def similarity(v1,v2):
	"Compute cosine similarity between two vectors"
	return np.dot(matutils.unitvec(v1),matutils.unitvec(v2))

def analyzetweets():
	model = loadmodel()
	sentimentvectors = getsentimentvectors(model)
	stopwords = getstopwords()
	with open('sentimentanalysis.tsv','w') as f1:
		sys.stdout = f1
		with open('preprocessedtweets.tsv','r') as f:
			print("created at","text",*sentimentvectors.keys(),sep='\t')
			for x in f:
				created_at,id,text = x.split('\t')
				words = [a for a in text[:-1].split() if a not in stopwords and model.__contains__(a)]
				if len(words) > 1:
					meanvec = KeyedVectors.get_mean_vector(model,words,pre_normalize=True,post_normalize=True,ignore_missing=False)
					differences = []
					for key,vector in sentimentvectors.items():
						differences.append(similarity(vector,meanvec))
					print(created_at,' '.join(words),*differences,sep='\t')

def getaggregates(interval='second',mindate=None,normalize=False):
	s = {'second':None,'minute':16,'hour':13,'day':10,'month':7,'year':4}[interval]
	with open('sentimentanalysis.tsv','r') as f1:
		with open(f"sentimentaggregates{interval}s.tsv",'w') as f2:
			sys.stdout = f2
			header = next(f1).split('\t')
			print(header[0],*header[2:],sep='\t',end='')
			totals,counts = {},{}
			for x in f1:
				created_at,text,*vecs = x[:-1].split('\t')
				if mindate and created_at < mindate:
					continue
				vecs = list(map(lambda f:float(f),vecs))
				date = created_at[:s]
				if date not in totals:
					totals[date] = vecs
					counts[date] = 1
				else:
					totals[date] = [a+b for a,b in zip(totals[date],vecs)]
					counts[date] += 1
			initials = None
			for day,count in counts.items():
				averages = list(map(lambda c:c/count,totals[day]))
				if not initials:
					initials = list(map(lambda c:c-0.05,averages))
				vectors = [a-b for a,b in zip(averages,initials)] if normalize else averages
				print(day,*vectors,sep='\t')

if __name__ == "__main__":
	analyzetweets()
	getaggregates(interval='month',mindate='2009',normalize=True)
