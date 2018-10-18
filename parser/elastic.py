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


    def postData(self, index='open-spam-email-dev', type='test_type', body={}, id=""):
        if not 'timestamp' in body:
            body['timestamp'] = datetime.datetime.utcnow()
        index = index + "-" + str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month)
        if id == "":
            res = self._es.index(index=index, doc_type=type, body=body)
        else:
            res = self._es.index(index=index, id=id, doc_type=type, body=body)
        return res