import http.client
import json
import re
from urllib.parse import urlparse

def get_urls(msg):
    print(msg)
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)
    return urls

def reputation(domain):
    try:
        conn = http.client.HTTPSConnection("domain-reputation-api.whoisxmlapi.com")
        conn.request("GET", "https://domain-reputation-api.whoisxmlapi.com/api/v1?apiKey=at_8ZUulDTGkDRupfIbzOHXVnrNY0tWI&domainName={}".format(domain))
        res = conn.getresponse()
        if res.reason == "OK":
            str = res.read()
            j = json.loads(str)
        return int(j['reputationScore'])
    finally:
        print("closing")
        conn.close()
