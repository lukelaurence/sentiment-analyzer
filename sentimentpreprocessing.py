def containsbad(input):
	acceptable = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'_\n"
	for x in input:
		if x not in acceptable:
			return True
	return False

def getphrases(sorted = False):
	phrases = []
	with open('index_to_key.txt','r') as f:
		for x in f:
			if '_' in x and not containsbad(x) and x[-2] != '_' and x[0] != '_':
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
	acceptable = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'"
	output = [' '] #space terminators due to underscore-demarcated phrases
	lastcharspace = True
	for x in input:
		out = x if x in acceptable else ' '
		if lastcharspace and out == ' ':
			continue
		lastcharspace = (out == ' ')
		output.append(out)
	output.append(' ') #space terminators due to underscore-demarcated phrases
	return ''.join(output)

def preprocesstext(phrases,input):
	text = strippunctuation(input)
	for underscore,space in phrases:
		if space in text:
			text = text.replace(space,underscore)
	return text[1:-1]

def preprocess(phrases,seen,tweet):
	created_at = tweet[16:40]
	midvalue = 50+tweet[50:].find("'")
	id = int(tweet[50:midvalue])
	if id not in seen:
		seen.add(id)
		text = tweet[midvalue+12:-3]
		text = preprocesstext(phrases,text)
		print(f"{created_at}\t{id}\t{text}")

def preprocesstweets():
	phrases = getphrasetuples()
	with open('historicoutput.txt','r') as f:
		seen_ids = set()
		for x in f:
			preprocess(phrases,seen_ids,x)

# if __name__ == "__main__":
# 	main()