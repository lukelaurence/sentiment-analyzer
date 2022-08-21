import requests, os, sys, time
from twittercredentials import set_credentials

set_credentials()
bearer_token = os.environ.get("BEARER_TOKEN")
search_url = "https://api.twitter.com/2/tweets/counts/all"

def constructquery(langtype):
	langcode = "TW" if langtype == 'traditional' else 'CN'
	querystring = "("
	with open(f"unique{langtype}.txt",'r') as f:
		for x in f:
			querystring += x[0]
			if len(querystring) >= 996:
				break
			querystring += " OR "
		querystring += f") lang:zh-{langcode} -is:retweet"
	return querystring

def bearer_oauth(r):
	r.headers["Authorization"] = f"Bearer {bearer_token}"
	r.headers["User-Agent"] = "v2FullArchiveTweetCountsPython"
	return r

def connect_to_endpoint(params):
	response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
	if response.status_code != 200:
		raise Exception(response.status_code, response.text)
	return response.json()

def getcounts(langtype):
	query_params = {'query':constructquery(langtype),'granularity':'day','start_time':'2006-04-01T00:00:00Z'}
	with open(f"{langtype}counts.txt",'w') as f:
		sys.stdout = f
		json_response = connect_to_endpoint(query_params)
		while True:
			try:
				query_params['next_token'] = json_response['meta']['next_token']
				json_response = connect_to_endpoint(query_params)
				for x in json_response['data']:
					print(x)
				time.sleep(3)
			except:
				break

def main():
	for x in ['simplified','traditional']:
		getcounts(x)

if __name__ == "__main__":
	main()