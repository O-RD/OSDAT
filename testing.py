from elasticsearch import Elasticsearch
import json


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


input = "1NwUjqNdrfkz5nrZZ1FYEHtidex1Xart95"

_hash = "2a6ede103277e9aa503d4a61058fd497fa06a362802086c64361ca10b4e3a803"

_index = "1"

search_output = {'match': {'outputAddress': input}}

search_transactionhash = {'match': {'TransactionID': _hash}}

search_tuple = {
                    'bool': {
                    'must': {'match': {'TransactionID': _hash}},
                    'filter': {'match': {'outputIndex': _index}}
                    }
                }

_es = connect_elasticsearch()

res = search(_es,"zeblytics",search_output)

print(res)

