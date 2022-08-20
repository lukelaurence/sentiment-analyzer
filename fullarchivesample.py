import requests
import os
from datetime import datetime, timedelta
from random import randint
import sys
import time
from twittercredentials import set_credentials

set_credentials()
bearer_token = os.environ.get("BEARER_TOKEN")
search_url = "https://api.twitter.com/2/tweets/search/all"

def bearer_oauth(r):
	"""
	Method required by bearer token authentication.
	"""

	r.headers["Authorization"] = f"Bearer {bearer_token}"
	r.headers["User-Agent"] = "v2FullArchiveSearchPython"
	return r

def connect_to_endpoint(params):
	response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
	if response.status_code != 200:
		raise Exception(response.status_code, response.text)
	return response.json()

def getjson(query_params):
	json_response = connect_to_endpoint(query_params)
	try:
		return json_response['data']
	except:
		return []

def cycledates(beginning,end):
	wrap = lambda x : x.strftime('%Y-%m-%dT%H:%M:%S.00Z')
	date = beginning
	query_params = {'query': '(\\"or\\" OR \\"and\\" OR the OR be OR to OR of OR a OR in OR that OR have OR I OR it OR for OR not OR on OR with OR he OR as OR you OR do OR at OR this OR but OR his OR by OR from OR they OR we OR say OR her OR she OR an OR will OR my OR one OR all OR would OR there OR their OR what OR so OR up OR out OR if OR about OR who OR get OR which OR go OR me OR when OR make OR can OR like OR time OR no OR just OR him OR know OR take OR people OR into OR year OR your OR good OR some OR could OR them OR see OR other OR than OR then OR now OR look OR only OR come OR its OR over OR think OR also OR back OR after OR use OR two OR how OR our OR work OR first OR well OR way OR even OR new OR want OR because OR any OR these OR give OR day OR most OR us) lang:en -is:retweet -is:nullcast','max_results':10,'tweet.fields': 'created_at'}
	while date < end:
		query_params['start_time']=wrap(date)
		query_params['end_time']=wrap(date + timedelta(hours=1))
		results = getjson(query_params)
		for x in results:
			print(x)
		date += timedelta(hours=randint(1,168),seconds=randint(0,3599))
		time.sleep(3)

def main():
	with open('historicoutput.txt','a') as f:
		sys.stdout = f
		cycledates(datetime(2006,4,1,0,0,0,0),datetime(2022,8,1,0,0,0,0))

if __name__ == "__main__":
	main()