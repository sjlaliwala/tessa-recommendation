import json
from os.path import exists
from config.table_names import *

def write_dict_to_json(dict, filename):
  with open(filename, 'w') as outfile:
    json.dump(dict, outfile, default=str)

def read_json_to_dict(filename):
  with open(filename, 'r') as infile:
    data = json.load(infile)
  return data

LOCAL_DB = {
  USERS : read_json_to_dict(f'{LOCAL_DB_PATH}/{USERS}.json') if exists(f'{LOCAL_DB_PATH}/{USERS}.json') else None,
  NEWS: read_json_to_dict(f'{LOCAL_DB_PATH}/{NEWS}.json') if exists(f'{LOCAL_DB_PATH}/{NEWS}.json') else None,
  PROFESSIONALS: read_json_to_dict(f'{LOCAL_DB_PATH}/{PROFESSIONALS}.json') if exists(f'{LOCAL_DB_PATH}/{PROFESSIONALS}.json') else None,
  RECOMMENDATIONS: read_json_to_dict(f'{LOCAL_DB_PATH}/{RECOMMENDATIONS}.json') if exists(f'{LOCAL_DB_PATH}/{RECOMMENDATIONS}.json') else None,
  TEST_USERS : read_json_to_dict(f'{LOCAL_DB_PATH}/{TEST_USERS}.json') if exists(f'{LOCAL_DB_PATH}/{TEST_USERS}.json') else None
}

def load_table(table):
  if table not in LOCAL_DB:
    print('NO TABLE EXISTS')
  else: 
    return LOCAL_DB[table]

def cache_table(table, data):
  write_dict_to_json(data, f'{LOCAL_DB_PATH}/{table}.json')

