#!/usr/bin/env python3.5
# coding: utf-8

"""
SD_Discrimination : Framework for Subgroup Discovery and detecting discrimination in datasets. Main function
"""

import sys, os, argparse, logging, pandas as pd
from sd import sd, sd_beamSearch
from discrimination import discrimination
from emm import emm ,emm_beamSearch

def parse_args():
  parser = argparse.ArgumentParser()
  parser = argparse.ArgumentParser(description='SD_Discrimination : Framework for Subgroup Discovery and detecting discrimination in datasets.')
  parser.add_argument('dataset',  metavar='dataset.csv', help='Path to dataset in CSV format')
  parser.add_argument('-d', '--debug', action='store_true', help='Activate debug mode')
  parser.add_argument('-sd', action='store_true', help='Run only Subgroup Discovery')
  parser.add_argument('-dd', action='store_true', help='Run only Direct Discrimination Detection')
  parser.add_argument('-id', action='store_true', help='Run only Indirect Discrimination Detection')
  parser.add_argument('-bs', action='store_true', help='Run BeamSearch (Only for SD or EMM)')
  parser.add_argument('-emm', action='store_true', help='Run only Exceptional Model Mining')

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

  #CONFIGURE READ_CSV FUNCTION TO READ THE CSV PROPERLY
  #----------------------------------------------------
  df = pd.read_csv(args.dataset,encoding = "ISO-8859-1",delimiter=';') 
  #----------------------------------------------------
  
  if args.sd:
    if args.bs:
      #Runs beamSearch for automatic SD
      sd_beamSearch(df)
    else:
      #Subgroup Discovery
      sd(df)
  elif args.dd:
    #Discrimination Analysis (Direct)
    discrimination (df)
  elif args.id:
    #Discrimination Analysis (Indirect)
    discrimination (df,True)
  elif args.emm:
    if args.bs:
      #Runs beamSearch for automatic EMM
      emm_beamSearch(df)
    else:
      #Exceptional Model Mining
      emm(df)
  sys.exit(0)

if __name__ == '__main__':
  main()