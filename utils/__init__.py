import zipfile
import subprocess
import csv
import os
import sys
from random import shuffle
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
real_path = os.path.realpath(__file__)
basedir = os.path.dirname(real_path)

def list_to_dict(header, row):
    if len(header) != len(row):
        raise IndexError("Make sure your data have the same size")
    res = {}
    for i, val in enumerate(header):
        res[val] = row[i]
    return res


def extract_files(path_to_zip_file, directory_to_extract_to):
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()

def download_adresses(adresses,sample = None ,outputdir=os.path.join(basedir,"../data/")):
    data_downloaded = -len(adresses)
    if sample:
        data_downloaded = - sample

    for link in adresses:
        if data_downloaded < 0:
            print link["processed"]
            retval = subprocess.call('wget -N {link} -P {outputdir}'.format(**{
                "link": link["processed"],
            "outputdir":outputdir}), shell=True)
            data_downloaded += 1

def get_data(filestat = os.path.join(basedir, "state.txt"),country = 'fr',all=False ):
    f = open(filestat, 'rb')
    reader = csv.reader(f, delimiter="\t")
    headers = reader.next()
    res = []
    for row in reader:
        row_dict = list_to_dict(headers,row)
        if country and row_dict['source'].startswith(country):
            res.append(row_dict)
        if all and row_dict not in res:
            res.append(row_dict)

    return res

def get_file_by_ext(dir,ext=".zip"):
    files=os.listdir(dir)
    return [ os.path.join(dir,_file) for _file in files if _file.endswith(ext)]

