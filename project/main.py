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



#analyze stuff


prompt_thingie = (f'''You are a professional html reader and summarizer, skilled in reading Privacy Policies. You will ignore all the unneccessary information not pertaining to the Privacy Policy in the file. Answer TRUE or FALSE to the following statements.
Information Sharing with Third Parties.
Data Selling.
Significant Data Retention.
Do Not Track Response not mentioned or available.
Opt Out Not Available completely.
Is not internationally available and uniform (look for flags that mark for certain regions having different policies).
Is a Public Platform/Social Media AND/OR User info available to other users. 
Settings to hide activity from other users NOT stated.
Explanation of privacy rights is not comprehensive.
Automated Decision making is taken.
Updates are not notified to users.
Access to your own data not available, or policy not mentioned.
Deletion of your data available, or policy not mentioned.
Explanation of purpose of data collection not given, not mentioned, or ambiguious.
Location data collected.
IP data collected.
Payment data collected. 
Is the data collected not relevant to the purpose specified in any place in this? 
Additionally, you should justify your response. You will do this by quoting or explaining a short section which led you to this judgement. Use tokens on this judgement FIRST before attempting to answer TRUE/False. Additionally, for statement 6 mention affected regions. Your response should be in the format of a 2d python list [[], []]. The first part will be an array of true and false booleans you had generated for each statement. The second will be an array of the justifications as strings you used. The dimensions of the 2d array should thus be 2x18. Do not generate any other response, including acknowledgement of this instruction or the attached file you will read to answer these questions. You will understand these instructions thoroughly and completely. There are to be no generalizations. Do not answer in a code snippet. Answer in plain text, even though you are generating a code list.
{json_data}''')
genai.configure(api_key="AIzaSyBfTeyoXqdKDTv-0S9auvehejBCMtrzaVQ") #ADD - ashleys code
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt_thingie)
input_string = response.text
trimmed_string = input_string[10:-4]
# Convert the resulting string to a list of characters
result_list = eval(str(trimmed_string))
response_cleannn = result_list
print(response_cleannn) #test!!


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

#safety rating?

#output json.


