import logging
import os
import subprocess 
import yaml
import pandas as pd
import datetime 
import gc
import re

def read_config_file(filepath):
  with open(filepath, 'r') as stream:
    try:
      return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logging.error(exc)

def replacer(string, char):
  pattern = char + '{2,}'
  string = re.sub(pattern, char, string)
  return string

def col_header_val(c,table_config):
  c.columns = c.columns.str.lower()
  c.columns = c.columns.str.replace('[^\w]','_',regex=True)
  c.columns = list(map(lambda x: x.strip('_'), list(c.columns)))
  c.columns = list(map(lambda x: replacer(x,'_'), list(c.columns)))
  expected_col = list(map(lambda x: x.lower(), table_config['columns']))
  expected_col.sort()
  c.columns =list(map(lambda x: x.lower(),  list(c.columns)))
  c = c.reindex(sorted(c.columns), axis=1)
  if len(c.columns) == len(expected_col) and list(expected_col) == list(c.columns):
    print("column name and column length validation passed")
    return 1

  else:
      print("column name and column length validation failed")
      mismatched_columns_file = list(set(c.columns).difference(expected_col))
      print("Following file columns are not in the YAML file", mismatched_columns_file)
      missing_YAML_file = list(set(expected_col).difference(c.columns))   
      print("Following YAML file are not in the file uploaded", missing_YAML_file)
  logging.info(f'c columns: {c.columns}')
  logging.info(f'c expected columns: {expected_col}')
  return 0
