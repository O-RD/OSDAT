from flask import Blueprint, render_template, request
import os
import json
from elasticsearch import Elasticsearch
from pymongo import MongoClient
import requests
from .utils import get_plot



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


def searchForAbuse(k):
    query = {'match': {'address': k}}
    res = search(es,'abusedaddress',query)
    print(res)
    if len(res) == 0:
        res = None
    print(res)
    if res is None:
        return '0'
    else:
        return res[0]['_source']['label']

es = connect_elasticsearch()


def tracing(inputAddress, hop):
    listofAddresses = []
    temp_listofAddresses = []
    d = []
    temp = []
    listofAddresses.append(inputAddress)
    # es = connect_elasticsearch()
    counter = 1
    while (counter<int(hop)):
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
                        temp.append(res[0]['_source']['outputAddress'])
                        temp.append(res[0]['_source']['value'])
                        
                        bit = searchForAbuse(res[0]['_source']['outputAddress'])
                        if bit=='0':
                            temp.append('0')
                            temp.append('-')
                        else:
                            temp.append('1')
                            temp.append(bit)
                        d.append(temp)
                        temp = []
                    except:
                        search_in = {'match': {'TransactionID': _hash}}
                        res = search(es,'zeblytics',search_in)
                        print(str(res[0]['_source']['outputAddress']) + ' transacted with a value of ' + str(res[0]['_source']['value']))
                        temp_listofAddresses.append(res[0]['_source']['outputAddress'])
                        temp.append(res[0]['_source']['outputAddress'])
                        temp.append(res[0]['_source']['value'])
                        
                        bit = searchForAbuse(res[0]['_source']['outputAddress'])
                        if bit=='0':
                            temp.append('0')
                            temp.append('-')
                        else:
                            temp.append('1')
                            temp.append(bit)
                        d.append(temp)
                        temp = []


            listofAddresses = []
            listofAddresses = temp_listofAddresses
            temp_listofAddresses = []

        print('END OF HOP: ' + str(counter))
        counter = counter + 1
    print(d)
    return tuple(d)








# def stats():
#     numbers = []
#     res = requests.get('http://localhost:9200/zeblytics/_count')
#     res = res.content.decode("utf-8")
#     number = json.loads(res)
#     obj1 = number["count"]

#     res = requests.get('http://localhost:9200/abusedaddress/_count')
#     res = res.content.decode("utf-8")
#     number = json.loads(res)
#     obj2 = number["count"]

#     total = obj1 + obj2
#     numbers.append(obj1)
#     numbers.append(obj2)
#     numbers.append(total)

#     return tuple(numbers)







headings = ("Address", "Amount (in Satoshis)", "Abused(0/1)", "Label (if abused)")
d = ()
views = Blueprint('views', __name__)
response = ()

@views.route('/')
def home():
    global response
    # res = requests.get('http://localhost:9200/zeblytics/_count')
    # res = res.content.decode("utf-8")
    # number = json.loads(res)
    # print(number["count"])
    # result = tuple(obj2)
    # response = stats()
    response = "7"
    return render_template("home.html", data= response)

@views.route('/BTC',methods=['GET','POST'])
def btc():
    if request.method == 'POST':
        global d
        address = request.form.get('btcAddress')
        hops = request.form.get('BTChops')
        d = tracing(address,hops)
    return render_template("btc.html", headings=headings, data=d)

@views.route('/ETH')
def eth():
    return render_template("eth.html")




#1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp	