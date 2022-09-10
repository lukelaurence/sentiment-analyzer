def containsbad(input):
	acceptable = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_\n"
	for x in input:
		if x not in acceptable:
			return True
	return False

def getphrases(sorted=False):
	phrases = []
	with open('index_to_key.txt','r') as f:
		for x in f:
			if '_' in x and not containsbad(x) and '__' not in x and x[-2] != '_' and x[0] != '_':
				phrases.append(x) if sorted else print(x,end='')
	if sorted:
		phrases.sort(key=len,reverse=True)
		for x in phrases:
			print(x,end='')

def getphrasetuples():
	phrases = []
	with open('phrases.txt','r') as phrasefile:
		for phrase in phrasefile:
			p = phrase[:-1]
			phrases.append((' '+p+' ',' '+p.replace("_"," ")+' '))
	return phrases

def strippunctuation(input):
	acceptable = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	output = [' ']
	lastcharspace = True
	for x in input:
		out = x if x in acceptable else ' '
		if (lastcharspace and out == ' ') or x == "'":
			continue
		lastcharspace = (out == ' ')
		output.append(out)
	output.append(' ')
	return ''.join(output)

def getphraseindicies(phrases):
	indicies = {}
	for index,(u,s) in enumerate(phrases):
		l = len(u)
		if l not in indicies.keys():
			indicies[l] = index
	indicies.pop(max(indicies.keys()))
	return indicies

def get_max_and_min(input):
	max = float('-inf')
	min = float('inf')
	for x in input:
		if x > max:
			max = x
		if x < min:
			min = x
	return(max,min)

def sorttweets():
	with open('preprocessedtweets.tsv','r') as f:
		tweets = []
		for x in f:
			tweets.append(tuple(x.split('\t')))
		tweets.sort(key=lambda a:a[0])
	for a,b,c in tweets:
		print(f"{a}\t{b}\t{c}",end='')

def getaggregates(interval='second'):
	s = {'second':None,'minute':16,'hour':13,'day':10,'month':7,'year':4}[interval]
	with open('sentimentanalysis.tsv','r') as f:
		header = next(f).split('\t')
		print(header[0],*header[2:],sep='\t',end='')
		totals,counts = {},{}
		for x in f:
			created_at,text,*vecs = x[:-1].split('\t')
			vecs = list(map(lambda f:float(f),vecs))
			date = created_at[:s]
			if date not in totals:
				totals[date] = vecs
				counts[date] = 1
			else:
				totals[date] = [a + b for a,b in zip(totals[date],vecs)]
				counts[date] += 1
		for day,count in counts.items():
			print(day,*map(lambda c:c/count,totals[day]),sep='\t')

def preprocesstext(phrases,phrase_idxs,term_idxs,input):
	text = strippunctuation(input)
	l = len(text)
	p = phrases[phrase_idxs[l]:] if term_idxs[0]>l>term_idxs[1] else phrases
	for underscore,space in p:
		if space in text:
			text = text.replace(space,underscore)
	return text[1:-1]

def preprocesstweet(phrases,phrase_idxs,term_idxs,seen,tweet):
	created_at = tweet[16:40]
	midvalue = 50+tweet[50:].find("'")
	id = int(tweet[50:midvalue])
	if id not in seen:
		seen.add(id)
		text = tweet[midvalue+12:-3]
		text = preprocesstext(phrases,phrase_idxs,term_idxs,text)
		print(f"{created_at}\t{id}\t{text}")

def preprocesstweets():
	phrases = getphrasetuples()
	phrase_idxs = getphraseindicies(phrases)
	term_idxs = get_max_and_min(phrase_idxs.keys())
	with open('rawtweets.txt','r') as f:
		seen_ids = set()
		for x in f:
			preprocesstweet(phrases,phrase_idxs,term_idxs,seen_ids,x)
