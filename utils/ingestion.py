from conf import settings
from datetime import datetime
import csv
import os
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
real_path = os.path.realpath(__file__)
basedir = os.path.dirname(real_path)

def ingest_data(es, _type="fr", _index="openadress",
                filename=os.path.join(basedir, "../data/fr/aisne.csv"),
                batch=100,
                delimiter=",",sample_batch = 200):
    """
    
    :param es: 
    :param _type: 
    :param _index: 
    :param filename: 
    :param batch: 
    :param delimiter: 
    :return: 
    """
    f = open(filename, 'rb')
    reader = csv.reader(f, delimiter=delimiter)
    headers = reader.next()
    join_adress = ['NUMBER', 'STREET', 'UNIT', 'CITY', 'DISTRICT', 'REGION', 'POSTCODE']
    counter = 0
    bt_ = []
    for row in reader:
        tmp = {"_type": _type, "_index": _index}
        for key, val in zip(headers, row):
            tmp[key] = val
        tmp['_id'] = tmp['HASH']
        tmp['location'] = {'lat': float(tmp['LAT']), 'lon': float(tmp['LON'])}
        tmp['timestamp'] = datetime.now()
        tmp['adress'] = ' '.join([tmp[key] for key in join_adress])
        # for french
        tmp['REGIONCODE'] = tmp['POSTCODE'][:2]
        if tmp['UNIT'].strip() != '':
            print tmp
        bt_.append(tmp)
        if len(bt_) == batch:
            settings.helpers.bulk(es, bt_)
            counter += len(bt_)
            bt_ = []
        if sample_batch and counter > sample_batch:
            break
    settings.helpers.bulk(es, bt_)
