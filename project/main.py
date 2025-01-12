#hAWK TUAH!
#welcome
import polipy
from bs4 import BeautifulSoup
import requests
import re
import json
import os
import google.generativeai as genai
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
search = website_name + ' privacy policy'
url = 'https://www.duckduckgo.com/html/search/?q='+search

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
}

page = requests.get(url, headers=headers).text
soup = BeautifulSoup(page, 'html.parser').find_all("a", class_="result__url", href=True)

for link in soup:
    print(link['href'])
    break


#extract policy
url_analyzed = link['href']
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

response_cleannn.append(['Information sharing with Third Parties.', 'Data selling', 'Significant Data Retention', 'Do Not Track Response not mentioned or available', 'Opt Out not available completely.', 'Is not internationally available and uniform.', 'Is a Public Platform/Social Media AND/OR User info available to other users.', 'Settings to hide activity from other users NOT stated.', 'Explanation of privacy rights is not comprehensive.', 'Automated decision making is taken.', 'Updates are not notified to users.', 'Access to your own data not available, or policy not mentioned.', 'Deletion of your data not available, or policy not mentioned.', 'Explanation of purpose of data collection not given, not mentioned, or ambiguious.', 'Location data collected.', 'IP data collected.', 'Payment data collected.', 'Irrelevant data collection.'])
response_cleannn.append(['No/Limited information sharing with Third Parties.', 'No data selling at all', 'No or Extremely Short Data Retention', 'Do Not Track Response mentioned positively or available', 'Opt Out completely available.', 'Is internationally available and uniform', 'Other users do not interact with your data.', 'Settings to hide activity from other users stated.', 'Explanation of privacy rights is comprehensive.', 'Automated Decision making is not taken.', 'Updates are notified to users.', 'Access to your own data available.', 'Deletion of your data available.', 'Explanation of purpose of data collection is clear.', 'Location data not collected.', 'IP data not collected.', 'Payment data not collected or payment data not mentioned.', 'All data colection is relevant'])

# Specified keys for the JSON structure
keys = ["boolean", "judgement", "con", "pro"]


# Transpose the 2D list to group elements by their index
transposed_data = list(zip(*response_cleannn))

# Create the JSON structure
result_blob = {"user": [dict(zip(keys, values)) for values in transposed_data]}

# Convert to JSON string (for saving or display purposes)
json_output = json.dumps(result_blob, indent=4)

# Save to a file (optional)
with open("tableQuickfest.json", "w") as file:
    file.write(json_output)


def news_Fetch():
    search = website_name + ' data leaks recent news reports'
    url = 'https://www.duckduckgo.com/html/search/?q='+search

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
    }

    page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page, 'html.parser').find_all("a", class_="result__url", href=True)
    counter_thing=0
    results=[]

    for link in soup:
        results.append(link['href'])
        counter_thing+=1
        if counter_thing>=50:
            break
    print(results)
    titlearray=[]

    for i in range(len(results)-1):
        url_thinga = results[i]
        reqs = requests.get(url_thinga)
        soup_thang = BeautifulSoup(reqs.text, 'html.parser')
        for title in soup_thang.find_all('title'):
            temp_thanga = title.get_text()
            titlearray.append(temp_thanga)

    return [results, titlearray]

thingie=news_Fetch()
titlearray = thingie[1]
links= thingie[0]

keys=titlearray
values=links

# Build the JSON structure
json_structure = {
    "users": [{key: value} for key, value in zip(keys, values)]
}

# Convert the structure to a JSON string
json_string = json.dumps(json_structure, indent=4)

# Print the JSON string
with open("newsQuickfest.json", "w") as file:
    file.write(json_string)


notautistic = SentimentIntensityAnalyzer()
positiveScore = 0.5
for i in titlearray:
    sentiment_score = notautistic.polarity_scores(i)
    print(sentiment_score)
    positiveScore = positiveScore + sentiment_score['compound']

def analysis():
    if positiveScore/50 < 0:
        return ('The media does not seem to happy about this one...')
    else:
        return ('There is not too much hateful rhetoric in the media this time...')

analysis_report = analysis()
genai.configure(api_key="AIzaSyBfTeyoXqdKDTv-0S9auvehejBCMtrzaVQ") #ADD - ashleys code
response_no = model.generate_content(f"Generate a response of an integer between 0 and 100 rating data security on {name}. Only respond with this number and nothing else.")

clean_no = int(re.sub(r"[^0-9]", "", response_no))

json_data = {
    "score": clean_no,
    "analysis": analysis_report
}


# Save the JSON structure to a file
with open("scoringQuickfest.json", "w") as json_file:
    json.dump(json_data, json_file, indent=4)


