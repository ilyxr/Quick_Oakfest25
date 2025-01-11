#hAWK TUAH!
#welcome
import polipy
from bs4 import BeautifulSoup
import requests
import re
import json
import os
import google.generativeai as genai
import newsapi

#retrieve website

website_input = input("Input/Paste a website hyperlink. ")
def get_domain(website_input):
    """Extracts the domain from the website hyperlink, including https://."""
    # Use regex to match the domain
    match = re.match(r'(https?://[a-zA-Z0-9.-]+)', website_input)
    if match:
        return match.group(1)
    return None

def get_name_from_domain(domain):
    """Extracts the name from the domain."""
    # Remove the https:// or http:// part
    domain_name = domain.split("://")[-1]
    
    # Split the domain by periods
    parts = domain_name.split('.')
    
    # If the domain has two periods, return the middle part
    if len(parts) >= 3:
        return parts[-2]
    # Otherwise, return the first part
    return parts[0]

domain = get_domain(website_input)
if domain:
    name = get_name_from_domain(domain)
    print(f"Domain: {domain}")
    print(f"Name: {name}")
else:
    print("Invalid website hyperlink.")



#conduct search
website_name = name
search = website_name + 'privacy policy'
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


for root, directories, files in os.walk('.', topdown=True):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                json_data = json.load(f)

data_1 = json.loads(json_data)
result = data_1["text"]
extracted_text= result

#analyze policy
prompt_thingie = ('do not respond to the following text. just say hi. this is for a test. ' + extracted_text)
genai.configure(api_key="AIzaSyCeP4d9MvojRJDwTHZK4JAYRceHPdwY0Js") #ADD - ashleys code
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt_thingie)
print(response.text) #test!!



#transform gemini output to readable data




#news pull

def news_Fetch():
    search = website_name + ' data leaks recent news reports'
    url = 'https://www.google.com/search'

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
    }
    parameters = {'q': search}
    content = requests.get(url, headers=headers, params=parameters).text
    soup = BeautifulSoup(content, 'html.parser')


    search_results = soup.find_all('div', class_='tF2Cxc')


    results = []
    for result in search_results[:5]:
        title = result.find('h3').text if result.find('h3') else 'No title'
        link = result.find('a')['href'] if result.find('a') else 'No link'
        description = result.find('span', class_='aCOpRe').text if result.find('span', class_='aCOpRe') else 'No description'
        results.append({'title': title, 'link': link, 'description': description})

    for i, res in enumerate(results, start=1):
        print(f"Result {i}:")
        print(f"Title: {res['title']}")
        print(f"Link: {res['link']}")
        #print(f"Description: {res['description']}\n") --- defunct bruh

news_Fetch()

#safety rating
