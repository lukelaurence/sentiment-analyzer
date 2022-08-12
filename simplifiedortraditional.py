import requests
import os
import json
import hanzidentifier
from twittercredentials import set_credentials

set_credentials()

bearer_token = os.environ.get("BEARER_TOKEN")

def create_url():
	return "https://api.twitter.com/2/tweets/sample/stream"


def bearer_oauth(r):
	"""
	Method required by bearer token authentication.
	"""

	r.headers["Authorization"] = f"Bearer {bearer_token}"
	r.headers["User-Agent"] = "v2SampledStreamPython"
	return r

KATAKANA_CHARS = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
HIRAGANA_CHARS = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわゐゑをんっゝ"

def contains_japanese(string):
	for x in KATAKANA_CHARS:
		if x in string:
			return True
	for x in HIRAGANA_CHARS:
		if x in string:
			return True
	return False

def connect_to_endpoint(url):
	tweets = dict()
	response = requests.request("GET", url, auth=bearer_oauth, stream=True)
	tradcount,simpcount = 0,0
	for response_line in response.iter_lines():
		if response_line:
			json_response = json.loads(response_line)
			tweets[json_response['data']['id']] = json_response['data']['text']
			# print(json_response['data']['text'].replace('\n'," "))
			a = json_response['data']['text']
			if hanzidentifier.has_chinese(a):
				if not contains_japanese(a):
					chartype = hanzidentifier.identify(a)
					if chartype == 1: #traditional
						tradcount += 1
					elif chartype == 2: #simplified
						simpcount += 1
		print(tradcount,simpcount)
	if response.status_code != 200:
		raise Exception(
			"Request returned an error: {} {}".format(
				response.status_code, response.text
			)
		)
	return tweets


def maketweets():
	url = create_url()
	timeout = 0
	tweets = dict()
	while True:
		tweets |= connect_to_endpoint(url)
		timeout += 1
		if timeout >= 1:
			break
	return tweets


if __name__ == "__main__":
	maketweets()

maketweets()
