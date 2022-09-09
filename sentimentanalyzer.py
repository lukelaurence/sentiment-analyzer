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
		for x in f:
			head,*tail = x.split('\t')[:-1]
			for y in tail:
				if not model.__contains__(y):
					raise Exception(f"{y} is not in model")
			sentimentvectors[head] = KeyedVectors.get_mean_vector(model,tail,pre_normalize=True,post_normalize=True,ignore_missing=False)
	return sentimentvectors

def similarity(v1,v2):
	"Compute cosine similarity between two vectors"
	return np.dot(matutils.unitvec(v1),matutils.unitvec(v2))

def analyzetweets():
	model = loadmodel()
	with open('sentimentanalysis.tsv','w') as f1:
		sys.stdout = f1
		sentimentvectors = getsentimentvectors(model)
		with open('preprocessedtweets.tsv','r') as f:
			stopwords = getstopwords()
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

if __name__ == "__main__":
	analyzetweets()
