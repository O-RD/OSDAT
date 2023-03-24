#from pymongo import MongoClient
from elasticsearch import Elasticsearch

try:
    client = Elasticsearch([{'host': 'localhost', 'port': 9200,"scheme": "http"}])
    print('Connected to Elasticsearch')
    #db = client['Zeblytics']
except:
    print("Error in connecting to database")



#db = client['Zeblytics']
db = client.indices.get(index='zeblytics')


collection = client.search(index='zeblytics', body={'query': {'match_all': {}}},size=10000)

#total = collection.count()
total = client.count(index='zeblytics')['count']


counter = 1

for d in collection['hits']['hits']:
    inputHash = d['_source']['inputHash']
    inputIndex = d['_source']['inputIndex']
    print(d['_source']['outputAddress'])
    if inputHash == '0000000000000000000000000000000000000000000000000000000000000000':
        query = {
                "$set": {
                    "inputAddress": 'ORIGIN'
                }
            }
        collection.update_one(d, query)

    else:
        try:
            search_result = client.search(index='zeblytics', body={'query': {'bool': {'must': [{'match': {'TransactionID': inputHash}}, {'match': {'outputIndex': inputIndex}}]}}})
            if search_result['hits']['total']['value'] == 1:
                search_hit = search_result['hits']['hits'][0]
                search_id = search_hit['_id']
                client.update(index='zeblytics', id=search_id, body={'doc': query})
            print('Updated')
        except:
            query = {
                "$set": {
                    "inputAddress": 'ORIGIN'
                }
            }
            collection.update_one(d, query)
    print('Updated: ' + str(counter) + '/' + str(total))
    print('   ')
    counter = counter + 1
