from gensim.models import KeyedVectors
from gensim.parsing.preprocessing import STOPWORDS
from gensim import matutils
import numpy as np
import os.path

model = KeyedVectors.load_word2vec_format(os.path.join(os.path.dirname(__file__),os.pardir,'GoogleNews-vectors-negative300.bin'),binary=True)

def getsentimentvectors():
	sentimentvectors = {}
	with open('sentiment_vectors.tsv','r') as f:
		for x in f:
			y = x.split('\t')
			sentimentvectors[y[0]] = KeyedVectors.get_mean_vector(model,y[1:],pre_normalize=True,post_normalize=True,ignore_missing=False)

def similarity(v1,v2):
	"Compute cosine similarity between two vectors"
	return np.dot(matutils.unitvec(v1),matutils.unitvec(v2))

def importtweets():
	sentimentvectors = getsentimentvectors()
	with open('preprocessedtweets.tsv','r') as f:
		print("created at","text",*sentimentvectors.keys(),sep='\t')
		for x in f:
			created_at,id,text = x.split('\t')
			words = [a for a in text.split() if a not in STOPWORDS and model.__contains__(a)]
			if len(words) > 1:
				meanvec = KeyedVectors.get_mean_vector(model,words,pre_normalize=True,post_normalize=True,ignore_missing=False)
				differences = []
				for key,vector in sentimentvectors.items():
					differences.append(similarity(vector,meanvec))
				print(created_at,text,*differences,sep='\t')
