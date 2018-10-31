from elasticsearch import Elasticsearch
import datetime
import simplejson as json
import certifi
import os

class Elastic:

    def __init__(self):
        # hostname = os.environ.get('ES_SERVER_ENDPOINT', 'search-emailbackend-27xthdgmoqc4o3h637lbzy6jhm.eu-west-1.es.amazonaws.com')
        # port = "443"
        # self._es = Elasticsearch([{"host":hostname, "port":port}], scheme="https", ca_certs=certifi.where())
       
        hostname = os.environ.get('ES_SERVER_ENDPOINT', 'localhost')
        port = "9200"
        self._es = Elasticsearch([{"host":hostname, "port":port}])

    def getLastDocument(self, index='open-spam-email-dev'):
        res = self._es.search(index=index, body={"query": {"match_all": {}}, "size": 1, "sort": [{"timestamp": {"order": "desc"}}]})
        return res

    def getDocuments(self, index='open-spam-email-dev*', from_doc=0, size_doc=10):
        res = self._es.search(index=index, body={"query": {"match_all": {}}, "size": size_doc, "from":from_doc})
        return res