import json
from elasticsearch import Elasticsearch
from pymongo import MongoClient
import json
import requests

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200,"scheme": "http"}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es

def search(es_object, index_name, search):
    res = es_object.search(index=index_name, query=search)
    all_hits = res['hits']['hits']
    response = json.dumps(all_hits)
    res = json.loads(response)
    return res


inputAddress = input("Enter the address you wish to track: ")
hops = int(input("Enter the number of hops: "))

print("Starting to track the address: " + inputAddress)

listofAddresses = []
temp_listofAddresses = []

listofAddresses.append(inputAddress)
    

es = connect_elasticsearch()


counter = 1

res = requests.get('http://localhost:9200/zeblytics/_count')

res = res.content.decode("utf-8")
d = json.loads(res)
print(d["count"])

while (counter<hops):

    for i in listofAddresses:
        search_output = {'match': {'outputAddress': i}}
        res = search(es,'zeblytics',search_output)
        for k in res:
            _hash = k['_source']['inputHash']
            _index = k['_source']['inputIndex']
            # print(_hash + '    ' + str(_index))
            if _hash=='0000000000000000000000000000000000000000000000000000000000000000':
                print('ORIGIN')
            else:
                search_input = {
                    'bool': {
                    'must': {'match': {'TransactionID': _hash}},
                    'filter': {'match': {'outputIndex': _index}}
                    }
                }
                try:
                    res = search(es,'zeblytics',search_input)
                    #print(res)
                    print(str(res[0]['_source']['outputAddress']) + ' transacted with a value of ' + str(res[0]['_source']['value']))
                    temp_listofAddresses.append(res[0]['_source']['outputAddress'])
                except:
                    search_in = {'match': {'TransactionID': _hash}}
                    res = search(es,'zeblytics',search_in)
                    print(str(res[0]['_source']['outputAddress']) + ' transacted with a value of ' + str(res[0]['_source']['value']))
                    temp_listofAddresses.append(res[0]['_source']['outputAddress'])


        listofAddresses = []
        listofAddresses = temp_listofAddresses
        temp_listofAddresses = []
    print('END OF HOP: ' + str(counter))
    counter = counter + 1



#1NwUjqNdrfkz5nrZZ1FYEHtidex1Xart95

#16zfxSwbR8LxVUSseBd5Kd5QbcrNQqyyr2
#1FXPLMkzfjTTahtf1wCiVxGahVmpHD6yw4