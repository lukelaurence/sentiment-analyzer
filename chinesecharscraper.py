import requests
from bs4 import BeautifulSoup
import sys

forbidden = " \xa01234567890\n"
langs = ['simplified','traditional']
charlists = {}
for langtype in langs:
	chars = []
	for pagenum in range(1,21):
		url = f"https://www.learnchineseez.com/read-write/{langtype}/index.php?page={pagenum}"
		page = requests.get(url)
		soup = BeautifulSoup(page.text,'lxml')
		table = soup.findChildren()
		for x in table:
			t = x.text
			if len(t) == 1 and t not in forbidden and t not in chars:
				chars.append(t)
	charlists[f"{langtype}"] = chars.copy()
uniques = {'simplified':[],'traditional':[]}
uniquesimplified,uniquetraditional = [],[]
getuniques = lambda x,y:[uniques[x].append(a) for a in charlists[x] if a not in charlists[y]]
getuniques('simplified','traditional')
getuniques('traditional','simplified')
def writetofile(langtype):
	with open(f"unique{langtype}.txt",'w') as f:
		sys.stdout = f
		for x in uniques[langtype]:
			print(x)
writetofile('simplified')
writetofile('traditional')