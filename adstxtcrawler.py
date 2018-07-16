import subprocess
import os
import requests
from pymongo import MongoClient

        
def adstxt_crawler(text_file):
    
    # Open file of crawlable domains
    # Parse publisher name for later
    
    print("Gathering Domains")
    domains = open(text_file, 'r')
    urls = []
    print("Gathering Publishers")
    pub_names = []
    for url in domains:
        url = url.strip('\n')
        urls.append(url)
        a,b,c,d = url.split('.')
        pub_names.append(b)
    domains.close
    
    # Send GET request to each domain and save contents to unique file
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Content-Type': 'text/plian; charset+utf-8',
    }
    content_files = []
    i = 0
    print("Reading /ads.txt")
    while i != len(urls):
        req_file = open('{}.txt'.format(pub_names[i]), 'w+')
        content_files.append(req_file.name)
        r = requests.get(urls[i], headers=headers)
        req_file.write(r.text)
        req_file.close()
        i += 1
        continue
        
    # Initalize MongoDB and create DB
    print("Starting MongoDB")
    subprocess.call("./mongo.sh start", shell=True)
    client = MongoClient()
    db = client.adstxt
    collection = db.dataset
    
    # Parse, Validate, Post to DB
    
    # Assume data is initialy valid
    data_valid = 1
    
    for file in content_files:
        file_to_parse = open(file, 'r')
        for entry in file_to_parse:
            entry = entry.strip('\n')
            separator = '#'
            entry = entry.split(separator, 1)[0]
            delimiter = entry.count(',')
            
            if delimiter == 2:
                exchange, pub_act_id, relationship = entry.split(',')

            elif delimiter == 3:
                exchange, pub_act_id, relationship, cert_id = entry.split(',')
                            
            else:
                # Was a comment line, etc
                continue
    
adstxt_crawler("domains.txt")
    