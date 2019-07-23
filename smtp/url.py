import http.client
import json
import re
from urllib.parse import urlparse

# Returns list with url's in a text by using regular expression matching.
def get_urls(msg):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)
    return urls

# Returns reputationScore of a certain domain based on its score at whoisxmlapi.com
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
        conn.close()

# Returns a list containing all low-rep domains contained in a text.
def raise_rep(text):
    urls = get_urls(text)
    lowrep = []
    for url in urls:
        if reputation(url) < 60:
            lowrep.append(url)
    return lowrep
