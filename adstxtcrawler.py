import subprocess
import requests
import datetime
import os
from pymongo import MongoClient

  
# Initalize MongoDB and create DB
print("Starting MongoDB")
subprocess.call("./mongo.sh start", shell=True)
client = MongoClient()
db_name = 'adstxt'
db = client[db_name]
collection_name = 'ads_txt_collection'
collection = db[collection_name]
    
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
        'Content-Type': 'text/plain; charset+utf-8',
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
    
    # Parse, Validate, Post to DB

    for file in content_files:
        file_to_parse = open(file, 'r')
        for entry in file_to_parse:
            # Strip \n 
            entry = entry.strip('\n')
            # Ignore Comments
            separator = '#'
            entry = entry.split(separator, 1)[0]
            # Determine # of fields
            delimiter = entry.count(',')
    
            
            if delimiter == 2:
                # Determine field values
                exchange, pub_act_id, relationship = entry.split(',')
                # Validate and add to DB
                if len(exchange) > 3 and len(pub_act_id) > 1 and len(relationship) < 8:
                    publisher_name, junk = file.split('.')
                    db_entry = {
                        "publisher_name": publisher_name,
                        "exchange_name": exchange,
                        "publisher_acct_id": pub_act_id,
                        "relationship_type": relationship,
                        "certification_id": {},
                        "http_endpoint": "http://www.{}.com/ads.txt".format(publisher_name),
                        "date_of_entry": datetime.datetime.utcnow()
                    }
                    post = db.posts
                    post_id = post.insert_one(db_entry).inserted_id
                else:
                    # Data was malformed
                    continue
            
       
            elif delimiter == 3:
                # Determine field values
                exchange, pub_act_id, relationship, cert_id = entry.split(',')
                
                # Validate and add to DB
                if len(exchange) > 3 and len(pub_act_id) > 1 and len(relationship) < 8:
                    publisher_name, junk = file.split('.')
                    db_entry = {
                        "publisher_name": publisher_name,
                        "exchange_name": exchange,
                        "publisher_acct_id": pub_act_id,
                        "relationship_type": relationship,
                        "certification_id": cert_id,
                        "http_endpoint": "http://www.{}.com/ads.txt".format(publisher_name),
                        "date_of_entry": datetime.datetime.utcnow()
                    }
                    post = db.posts
                    post_id = post.insert_one(db_entry).inserted_id
                    
                    
                else:
                    
                    # Data was malformed
                    continue
            else:
                
                # Data was malformed
                continue
        os.remove(file)        
        print("Posts of {}/ads.txt sucessful".format(publisher_name)) 
        
    for name in pub_names:
        print(post.find_one({"publisher_name": name}, {"http_endpoint": 1}))
        
    
    
def main(text_file):
    adstxt_crawler(text_file)
    client.drop_database(db_name)
    subprocess.call("./mongo.sh stop", shell=True)
    
main("domains.txt")