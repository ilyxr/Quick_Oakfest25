#Cybersecurity is cancer

from google import genai
from google.genai import types
import httpx
import os
import base64
import json
import requests
import time
import urllib
from payloads import PAYLOADS
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from dotenv import load_dotenv
import math
import re
import sys 

load_dotenv()
###edge





#TESTING GEMINI




hubstring = str(input("Paste a valid Github URL: "))

def github_read_file(username, repository_name, file_path, github_token=None):
    headers = {}
    if github_token:
        headers['Authorization'] = f"token {github_token}"
        
    url = f'https://api.github.com/repos/{username}/{repository_name}/contents/{file_path}'
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    file_content = data['content']
    file_content_encoding = data.get('encoding')
    if file_content_encoding == 'base64':
        file_content = base64.b64decode(file_content).decode()

    return file_content


def hubrunner():
    github_token = os.environ['GITHUB_TOKEN']
    parsed = urlparse(hubstring)
    parts = parsed.path.strip('/').split('/')
    if len(parts) < 5 or parts[2] != "blob":
        raise ValueError("Invalid GitHub file URL format")
   
    username = parts[0]
    repository_name = parts[1]
    branch = parts[3]
    file_path = "/".join(parts[4:])
    file_content = github_read_file(username, repository_name, file_path, github_token=github_token)
    data = (file_content)
    #print(data)
    #dont need this rn
    return data

my_code_file_i_love_hu_tao = hubrunner()

###
#TEMPORARY PROMPT
prompt = "You are an expert cybersecurity analyst tasked with detecting weaknesses in codebases. You are to be given a code file where you must detect all the flaws. These flaws include leaked secrets like .env files or keys, vulnerable literal string interpretation, injection vulnerabilities, path traversal vulnerabilities, XSS security failures, deserialization vulnerabilities, symmetric encryption, outdated encryption algorithms, open ports, not using https or tls, sending sensitive data in query strings, typosquatting and outdated packages, Insecure Direct Object Reference, etc. This is no means a comprehensive list, but look out for them. This is the code to review: " + my_code_file_i_love_hu_tao + "  Once you have reviewed this, you are to report on it in a structured manner. Respond in a CSV format with each row having one error, represented by its line number which MUST be an integer, the  in the line word for word, and the reasoning and then solution. I also want a new last row to just to have your overall security score of this. This should be a number from 1-100 and ONLY a float. Do NOT use commas in your text responses. Dummy example row: 45, clientkey=totallymyclientkey9873824873849832848947432793248, The key is exposed and hardcoded and could be stolen., Use an environment file. Dummy example last row: 88"

api_key1 = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key1)
'''
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt
)

print(response.text)
'''
#TURN ON AT END





#TESTING SQLI





#like and sub

#me and epstein are working on this together, we are testing the endpoints for vulnerabilities using the payloads we have defined in the payloads.py file. We will be using the requests library to send requests to the endpoints and check for any vulnerabilities. We will be looking for things like SQL injection, XSS, and other common vulnerabilities. We will also be checking the response status codes and the response body for any signs of vulnerabilities.

#^ wtf did ai generate dawg i am NEVER using the autocomplete feature again lol

def find_inputs(base_url):
    endpoints = []
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")

    # find forms or smth idk
    for form in soup.find_all("form"):
        action = form.get("action")
        method = form.get("method", "get").lower()

        inputs = []
        for inp in form.find_all("input"):
            name = inp.get("name")
            if name:
                inputs.append(name)
        endpoints.append({
            "url": urljoin(base_url, action),
            "method": method,
            "inputs": inputs
        })

    #brotato
    parsed = urlparse(base_url)
    params = parse_qs(parsed.query)

    if params:
        endpoints.append({
            "url": base_url,
            "method": "get",
            "inputs": list(params.keys())
        })
    return endpoints

def test_endpoint(endpoint):
    findings = []
    for param in endpoint["inputs"]:
        for payload in PAYLOADS:
            data = {param: payload}

            try:
                if endpoint["method"] == "post":
                    r = requests.post(endpoint["url"], data=data)
                else:
                    r = requests.get(endpoint["url"], params=data)
                findings.append({
                    "param": param,
                    "payload": payload,
                    "status": r.status_code,
                    "response": r.text[:500]
                })
            except Exception as e:
                findings.append({
                    "param": param,
                    "payload": payload,
                    "error": str(e)
                })
    return findings

SQL_ERRORS = [
    "sql syntax",
    "mysql",
    "sqlite",
    "postgres",
    "unterminated",
    "odbc",
    "database error",
    "query failed"
]

def detect_issues(test_results):
    issues = []
    for result in test_results:
        if "response" in result:
            text = result["response"].lower()
            #daisy daisy give me your answer do
            #does this look like a SQL error to you?
            #if it does, im a lolicon too
            #damn is 
            #ENRIQUEEE

            for err in SQL_ERRORS:
                if err in text:
                    issues.append({
                        "param": result["param"],
                        "payload": result["payload"],
                        "issue": "Possible SQL injection",
                        "indicator": err
                    })

    return issues

def generate_report(issues):
    print("\nreport\n")
    if not issues:
        print("No obvious SQLi indicators detected.")
        return
    for i, issue in enumerate(issues, 1):
        print(f"{i}. Parameter: {issue['param']}")
        print(f"   Payload: {issue['payload']}")
        print(f"   Indicator: {issue['indicator']}")
        print("")

TARGET = ("http://localhost:8501/")

print("checking the following: :", TARGET)
endpoints = find_inputs(TARGET)
all_results = []
for ep in endpoints:
    print("Testing endpoint:", ep["url"])
    results = test_endpoint(ep)
    all_results.extend(results)
issues = detect_issues(all_results)
generate_report(issues)





#TESTING XSS





TARGET_URL = "http://localhost:8501"
PAYLOAD_FILE = "xss_payloads.txt"
SUBMISSION_URL = TARGET_URL + "/resultsPage"

vulnerabilities_found = []

def load_payloads(filepath):
    try:
        with open(filepath, 'r') as f:
            payloads = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        return payloads
    except FileNotFoundError:
        print(f"fuck: '{filepath}' not found.")
        return []

def scan_reflected_xss(base_url, payloads):
    global vulnerabilities_found
    print("\n scan for reflected xss or something")
    endpoint = f"{base_url}/reflected"
    param = "search"
    
    for payload in payloads:
        encoded_payload = urllib.parse.quote_plus(payload)
        full_url = f"{endpoint}?{param}={encoded_payload}"
        try:
            response = requests.get(full_url, timeout=5)
            if payload in response.text:
                finding = {
                    "type": "Reflected XSS",
                    "endpoint": endpoint,
                    "payload": payload,
                    "proof_url": full_url
                }
                vulnerabilities_found.append(finding)
                print(f"[+] VULNERABLE (Reflected): {endpoint}")
                print(f"    - Payload: {payload}")
                print("-" * 20)

        except requests.exceptions.RequestException as e:
            print(f"problem connecting to {full_url}: {e}")
            break

def scan_stored_xss(base_url, payloads):
    global vulnerabilities_found
    print("\n test stored xss")
    endpoint = f"{base_url}/stored"
    try:
        requests.post(endpoint, data={'comment': 'initial_clean_comment'})
        time.sleep(0.5)
    except requests.exceptions.RequestException:
        print("baseline for xss test failed.")
        return
    for payload in payloads:
        try:
            post_response = requests.post(endpoint, data={'comment': payload}, timeout=5)
            if post_response.status_code == 200:
                get_response = requests.get(endpoint, timeout=5)
                if payload in get_response.text:
                    finding = {
                        "type": "Stored XSS",
                        "endpoint": endpoint,
                        "payload": payload,
                        "proof_url": endpoint
                    }
                    vulnerabilities_found.append(finding)
                    print(f"++++++ goon VULNERABLE (Stored): {endpoint}")
                    print(f"    -> Payload: {payload}")
                    print("-" * 20)
        except requests.exceptions.RequestException as e:
            print(f"error during stored XSS test for payload '{payload}': {e}")
            break

def submit_results(submission_url, results):
    print("\n Submit results to server ###")
    if not results:
        print("No vulnerabilities to submit.")
        return
    try:
        response = requests.post(submission_url, json={'results': results}, timeout=5)
        if response.status_code == 200:
            print(f"Results successfully submitted to {submission_url}")
        else:
            print(f"failed to submit. server responded with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Error submitting results: {e}")

if __name__ == '__main__': #why am i using main lol i have NEVER used ts before i could jst delete it and the indentation but it would lowkey be funny if i kept it in
    payloads_to_test = load_payloads(PAYLOAD_FILE)
    if payloads_to_test:
        scan_reflected_xss(TARGET_URL, payloads_to_test)
        scan_stored_xss(TARGET_URL, payloads_to_test)
        print("\n scan done!")
        if vulnerabilities_found:
            print(f"Found {len(vulnerabilities_found)} potential vulnerabilities.")
            submit_results(SUBMISSION_URL, vulnerabilities_found)
        else:
            print("No vulnerabilities were detected.")
    else:
        print("Could not load payloads.")





#TESTING CRYPTO





SECRET_PATTERNS = [
    r'api[_-]?key\s*=\s*["\'].*["\']',
    r'password\s*=\s*["\'].*["\']',
    r'secret\s*=\s*["\'].*["\']',
    r'BEGIN PRIVATE KEY',
    r'aws_access_key_id',
]

WEAK_CRYPTO_PATTERNS = [
    r'md5\(', r'sha1\(', r'DES\(', r'RC4', r'AES\/ECB'
    ]

HARDCODED_KEY_PATTERNS = [r'key\s*=\s*["\'][A-Za-z0-9]{6,}["\']', r'iv\s*=\s*["\'][A-Za-z0-9]{6,}["\']',]

#def shannon_entropy_or_some_shi_bro(string):
#    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
#    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
#    return entropy
#this stuff AINT WORK
#def looks_like_secret(value):
#    return shannon_entropy_or_some_shi_bro(value) > 3.5 and len(value) > 20


def scan_content(content):
    issues = []
    lines = content.splitlines()
    for i, line in enumerate(lines):
        for pattern in SECRET_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append(("exposed a secret GASP", i+1, line.strip()))
        for pattern in WEAK_CRYPTO_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append(("Old ass encryption", i+1, line.strip()))

        for pattern in HARDCODED_KEY_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append(("Hardcode crypto lmaol", i+1, line.strip()))
        strings = re.findall(r'["\'](.*?)["\']', line)

        #for s in strings: LOL DOES NOT WORK
        #   if looks_like_secret(s):
        #       issues.append(("Possible secret", i+1, line.strip()))
    status = "FAIL" if issues else "PASS"
    return status, issues

hi_lol=my_code_file_i_love_hu_tao
status, issues = scan_content(hi_lol)
print(status)
#can use issues but not rn
