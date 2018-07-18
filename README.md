# Sysnopsis

A reference implementation ads.txt files given a list of URLs or domains. Each run of program spins up a MongoDB instance and adds to a database created in the file. Database is dropped after program has ran, but can be queried before dropping. 


# Installation

This project assumes the following

* Python 3 or better
* Python Requests Library (pip install requests)
* Latest MongoDB version (https://docs.mongodb.com/manual/installation/)

# To run

Once project has been downloaded:

python/python3 adstxtcrawler.py

- more options can & will be added at later date
- right now only runs on given list of domains
- only tests DB entries of given URLS/domains
