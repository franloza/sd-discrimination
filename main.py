#!/usr/bin/env python
# coding: utf-8

"""
SD_Discrimination : Framework for Subgroup Discovery and detecting discrimination in datasets. Main function
"""

import sys, os, argparse, logging, pandas as pd
from sd import sd

def parse_args():
  parser = argparse.ArgumentParser()
  parser = argparse.ArgumentParser(description='SD_Discrimination : Framework for Subgroup Discovery and detecting discrimination in datasets.')
  parser.add_argument('dataset',  metavar='dataset.csv', help='Path to dataset in CSV format')
  parser.add_argument('-d', '--debug', action='store_true', help='Activate debug mode')
  return parser.parse_args()

def init_logging(log_file, debug=True):
  if debug:
    logging.basicConfig(
      format='%(asctime)s %(funcName)s:%(lineno)d - %(message)s',
      datefmt="%H:%M:%S",
      stream=sys.stdout,
      level=logging.DEBUG)
  else:
    logging.basicConfig(
      format='%(asctime)s [%(levelname)s] %(module)s:%(funcName)s - %(message)s',
      #Console OR File
      stream=sys.stdout,
      #filename=log_file,
      datefmt="%Y-%m-%d %H:%M:%S",
      level=logging.INFO)

def main():
  args = parse_args()
  me = os.path.splitext(os.path.basename(__file__))[0]
  log_file = '{}.log'.format(me)
  init_logging(log_file, args.debug)
  logging.debug('Debug mode activated')
  logging.info('Loading data from file')
  df = pd.read_csv (args.dataset,sep=';',header=0)
  #Subgroup Discovery
  sd(df)
  sys.exit(0)

if __name__ == '__main__':
  main()