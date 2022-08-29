from gensim.models.doc2vec import Doc2Vec,TaggedDocument
import smart_open,multiprocessing,csv,sys

def convertcsv(filename):
	csv.field_size_limit(1048576)
	with open(f"{filename}.csv",'r') as f:
		with open(f"{filename}.tsv",'w') as f2:
			reader = csv.reader(f)
			sys.stdout = f2
			clean = lambda a:' '.join(a.split())
			for x in reader:
				print(f"{clean(x[5])}\t{clean(x[6])}")

class TaggedCorpus:
    def __init__(self,text_path):
        self.text_path = text_path

    def __iter__(self):
        for line in smart_open.open(self.text_path,encoding='utf8'):
            title, words = line.split('\t')
            yield TaggedDocument(words=words.split(),tags=[title])

documents = TaggedCorpus('all-the-news.tsv.gz')

workers = multiprocessing.cpu_count() - 1

model_dbow = Doc2Vec(dm=0,dbow_words=1,vector_size=200,window=8,epochs=10,workers=workers,max_final_vocab=1000000)
model_dm = Doc2Vec(dm=1,dm_mean=1,vector_size=200,window=8,epochs=10,workers=workers,max_final_vocab=1000000)

model_dbow.build_vocab(documents,progress_per=500000)
model_dm.reset_from(model_dbow)

model_dbow.train(documents,total_examples=model_dbow.corpus_count,epochs=model_dbow.epochs,report_delay=30*60)
model_dbow.save('doc2vec_dbow.model')

model_dm.train(documents,total_examples=model_dm.corpus_count,epochs=model_dm.epochs,report_delay=30*60)
model_dm.save('doc2vec_dm.model')