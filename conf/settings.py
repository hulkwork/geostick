from elasticsearch import Elasticsearch
from elasticsearch import helpers

cluster_master = "localhost"
master_port = 9200

es = Elasticsearch(
    [cluster_master],
    port=master_port
)


