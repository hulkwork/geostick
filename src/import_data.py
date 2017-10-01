from utils import get_data,download_adresses,get_file_by_ext,extract_files,ingestion
from conf import settings
import os
real_path = os.path.realpath(__file__)
basedir = os.path.dirname(real_path)


def ingest_by_country(filestat = os.path.join(basedir,'../data/state.txt'),country='fr',sample=None,batch=100
                      ,sample_batch=None):
    list_link = get_data(filestat=filestat,country=country)
    download_adresses(adresses=list_link[5:],sample=sample,outputdir=os.path.join(basedir,'../data'))
    file_to_extract = get_file_by_ext(os.path.join(basedir,'../data'))
    directory_to_extract_to = os.path.join(basedir,"../data")
    for path_to_zip_file in file_to_extract:
        extract_files(path_to_zip_file, directory_to_extract_to)
        os.remove(path_to_zip_file)
    for path_to_ingest_file in get_file_by_ext(os.path.join(basedir,'../data/%s'%country),ext=".csv"):
        ingestion.ingest_data(settings.es, _type=country, _index="openadress-%s"%country,
                    filename=path_to_ingest_file,
                    batch=batch,
                    delimiter=",",sample_batch=sample_batch)
        os.remove(path_to_ingest_file)


ingest_by_country(sample=1,batch=10,sample_batch=50)