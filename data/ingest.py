import csv
import os
import sys
from datetime import datetime

from conf import settings
from utils import list_to_dict

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
real_path = os.path.realpath(__file__)
basedir = os.path.dirname(real_path)




# ingest_data(settings.es)
# curl -XDELETE 'localhost:9200/twitter?pretty'
q = {
    "from": 0, "size": 10,
    "query": {
        "match": {
            "adress": {
                "query": None,
                "cutoff_frequency": 0.0001
            }
        }
    }
}





