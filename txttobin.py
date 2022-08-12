from gensim.models import KeyedVectors
import numpy as np

model = KeyedVectors(200,12287936)
a = False
with open("tencent-ailab-embedding-zh-d200-v0.2.0.txt",mode='r') as f:
	for x in f:
		if a:
			arr = x.split(" ")
			key = arr[0]
			values = np.array(arr[1:]).astype(float)
			model.add_vector(key,values)
			continue
		a = True

model.save_word2vec_format(fname="tencent-ailab-embedding-zh-d200-v0.2.0.bin",binary=True)