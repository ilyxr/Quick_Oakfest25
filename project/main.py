#hAWK TUAH!
#welcome
import polipy
from bs4 import BeautifulSoup
import requests



#retrieve website




#conduct search

search = 'discord privacy policy'
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

print(first_link['href'])




#extract policy
url_analyzed = str(first_link['href'])
result = polipy.get_policy(url, screenshot=True)

### result.save(output_dir='.')  <------ turn on when you want output file!!


#analyze policy




#transform gemini output to readable data




#news pull





#safety rating