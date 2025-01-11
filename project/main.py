#hAWK TUAH!
#welcome
import polipy
from bs4 import BeautifulSoup
import requests



#retrieve website




#conduct search

search = 'github privacy policy'
#placeholder search
url = 'https://www.google.com/search'

headers = {
	'Accept' : '*/*',
	'Accept-Language': 'en-US,en;q=0.5',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
}
parameters = {'q': search}

content = requests.get(url, headers = headers, params = parameters).text
soup = BeautifulSoup(content, 'html.parser')

search = soup.find(id = 'search')
first_link = search.find('a')






#extract policy
url_analyzed = str(first_link['href'])
print(url_analyzed)
result = polipy.get_policy(url_analyzed, screenshot=True)

result.save(output_dir='.')
import json
import os

for root, directories, files in os.walk('.', topdown=True):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                json_data = json.load(f)

print(json_data, "yay")


#analyze policy




#transform gemini output to readable data




#news pull

import requests
url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=861d77216ad448c79d0fd0f003550f43')
response = requests.get(url)



#safety rating