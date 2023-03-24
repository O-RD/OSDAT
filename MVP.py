import json
from elasticsearch import Elasticsearch
from pymongo import MongoClient

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200,"scheme": "http"}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es

def search(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)

# 18FDfyu3ritCRatvRLtb9GD8fugboJtTuP

hops = int(input("Enter number of hops: "))
inputAddress = input("Enter the address you wish to track: ")

print("Starting to track the address: " + inputAddress)

inputhashList = []
inputhashIndex = []
inputAddresses = []

inputAddresses.append(inputAddress)
for i in range(0,hops):
    es = connect_elasticsearch()
    print('Please wait while we prepare for the hop: ' + str(i+1))
    for j in range(0,len(inputAddresses)):
        addresses = collection.find({"outputAddress": inputAddresses[j]})
        search_object = {'query': {'match': {'outputAddress': inputAddresses[j]}}}
        # z = list(addresses)
        search(es, 'recipes', json.dumps(search_object))
        for address in addresses:
            inputhashList.append(address['inputHash'])
            inputhashIndex.append(address['inputIndex'])
    
    if(len(inputhashList) == 0):
        print('Cannot trace back!')
    else:
        inputAddresses = []
        for k in range(0,len(inputhashList)):
            try:
                tracedAddress = collection.find_one({'TransactionID': inputhashList[k], 'outputIndex': inputhashIndex[k]})
                x = tracedAddress['outputAddress']
                y = tracedAddress['value']
                print(x + ' transacted with a value of ' + str(y) + ' Satoshis')
                search = abused.find_one({"address": x})
                if search is not None:
                    print('The above address is found in abused list! ABORT!!!')
                    break
                inputAddresses.append(x)
            except:
                print('Cannot trace it back..!')

    inputhashList = []
    inputhashIndex = []
    print('                                   ')


    