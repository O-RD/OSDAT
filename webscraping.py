from elasticsearch import Elasticsearch
import requests
import numpy as np
from bs4 import BeautifulSoup
import json
from time import sleep
import logging


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200,"scheme": "http"}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es

def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(index=index_name, doc_type='_doc', document=record)
        #print(outcome)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))


# Manualling Scraping each label

# source_url = "https://www.walletexplorer.com/wallet/SatoshiDice.com/addresses"

# es = connect_elasticsearch()

# x = {"address": "1HXKgoVRdLPiK4icefjjfBRbuG9izKmkpK","label": "Gambling"}
# store_record(es,'gambling',x)

# for k in range(1,21):

#     page = requests.get(source_url + "?page=" +  str(k))

#     soup = BeautifulSoup(page.text, 'html.parser')


#     tr = soup.find_all('tr')
#     print("Scraped: " + str(k) + "/20")
#     for c in tr:
#         try:
#             wallet_id = c.find('td').text
#             x = {"address": wallet_id,"label": "Gambling"}
#             store_record(es,'gambling',x)
#         except:
#             pass
#     sleep(10)
    

# Automatically Scraping each label

import requests
import numpy as np
from bs4 import BeautifulSoup

source_url = "https://www.walletexplorer.com/"

pages = [1,2,3,4,5]

temp = []
es = connect_elasticsearch()

for page in pages:

    services = [
    f'{source_url}wallet/{s["href"].rsplit("/")[-1]}/addresses?page=' + str(page) for s
    in BeautifulSoup(
        requests.get(source_url).text,
        "html.parser",
    ).select("table.serviceslist td ul li a")
]
    for service in services:
        temp.append(service)

counter = 1


total = len(temp)
for k in temp:
    s = BeautifulSoup(requests.get(k).text, "html.parser")
    print('Scraped: ' + str(counter) + '/' + str(total))
    for i in s.find_all("td"):
        if i.find("a"):
            wallet_id = i.find("a").getText()
            x = {"address": wallet_id, "label": k.rsplit('/')[-2]}
            store_record(es,'abusedaddress',x)

    sleep(10)
    counter = counter + 1
