import json
from elasticsearch import Elasticsearch
from pymongo import MongoClient
import logging


try:
    client = MongoClient('localhost',27017)
    print('Connected to Mongodb')
except:
    print("Error in connecting to database")


db = client.Zeblytics
collection = db.addressData

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


_es = connect_elasticsearch()


if(_es.ping()):
    i = 1
    doc = collection.find({},{'_id': 0,'inputAddress':0},limit=5000000)
    for x in doc:
        try:
            print('Indexed ' + str(i) + '/5000000')
            store_record(_es,'zeblytics',x)
            collection.delete_one(x)
            i = i + 1
        except:
            pass