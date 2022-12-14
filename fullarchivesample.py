import requests,os,sys,time
from datetime import datetime, timedelta
from random import randint
from twittercredentials import set_credentials
from sentimentpreprocessing import getphrasetuples,getphraseindicies,get_max_and_min,preprocesstext

set_credentials()
bearer_token = os.environ.get("BEARER_TOKEN")
search_url = "https://api.twitter.com/2/tweets/search/all"

def bearer_oauth(r):
	"Method required by bearer token authentication"
	r.headers["Authorization"] = f"Bearer {bearer_token}"
	r.headers["User-Agent"] = "v2FullArchiveSearchPython"
	return r

def connect_to_endpoint(params):
	response = requests.request("GET",search_url,auth=bearer_oauth,params=params)
	if response.status_code != 200:
		raise Exception(response.status_code,response.text)
	return response.json()

def getjson(query_params):
	json_response = connect_to_endpoint(query_params)
	try:
		return json_response['data']
	except:
		return []

def get_ids():
	unique_ids = set()
	with open('preprocessedtweets.tsv','r') as f:
		for x in f:
			unique_ids.add(x.split('\t')[1])
	return unique_ids

def cycledates(beginning):
	wrap = lambda x : x.strftime('%Y-%m-%dT%H:%M:%S.00Z')
	date = beginning
	query_params = {'query':'(\\"or\\" OR \\"and\\" OR is OR are OR the OR be OR to OR of OR a OR in OR that OR have OR I OR it OR for OR not OR on OR with OR he OR as OR you OR do OR at OR this OR but OR his OR by OR from OR they OR we OR say OR her OR she OR an OR will OR my OR one OR all OR would OR there OR their OR what OR so OR up OR out OR if OR about OR who OR get OR which OR go OR me OR when OR make OR can OR like OR time OR no OR just OR him OR know OR take OR people OR into OR year OR your OR good OR some OR could OR them OR see OR other OR than OR then OR now OR look OR only OR come OR its OR over OR think OR also OR back OR after OR use OR two OR how OR our OR work OR first OR well OR way OR even OR new OR want OR because OR any OR these OR give OR day OR most OR us) lang:en -is:retweet -is:nullcast','max_results':10,'tweet.fields': 'created_at'}
	end = datetime.today()-timedelta(days=2)
	unique_ids = get_ids()
	phrases = getphrasetuples()
	phraseindicies = getphraseindicies(phrases)
	term_idxs = get_max_and_min(phraseindicies.keys())
	f = sys.stdout
	t = time.time()
	with open('rawtweets.txt','a') as f1:
		with open('preprocessedtweets.tsv','a') as f2:
			while date < end:
				query_params['start_time']=wrap(date)
				query_params['end_time']=wrap(date+timedelta(hours=1))
				results = getjson(query_params)
				td = time.time()-t
				if td < 3:
					time.sleep(3-td)
				t = time.time()
				for x in results:
					id = x['id']
					if id in unique_ids:
						continue
					else:
						unique_ids.add(id)
						sys.stdout = f1
						print(x)
						sys.stdout = f2
						print(f"{x['created_at'][:19]}\t{id}\t{preprocesstext(phrases,phraseindicies,term_idxs,x['text'])}")
						sys.stdout = f
				date += timedelta(hours=randint(1,720),seconds=randint(1,2592000))

if __name__ == "__main__":
	while True:
		cycledates(datetime(randint(2006,2007),randint(4,12),randint(1,28),randint(0,23),randint(0,59),0,0))
