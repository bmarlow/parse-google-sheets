import httplib2
import os
import argparse
import json
import csv

from googleapiclient import discovery, errors
from google.oauth2 import service_account

# create argparse object and define args
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--auth", help="authentication dictionary", dest='auth')
parser.add_argument("-s", "--spreadsheet_id", help="authentication dictionary", dest='spreadsheet_id')
parser.add_argument("-r", "--range", help="authentication dictionary", dest='range')
parser.add_argument("-p", "--pod", help="the abbreviated pod name, eg: nws,swe, we", dest='pod' )
parser.add_argument("-t", "--timestamp", help="a timestamp to avoid file collissions", dest='timestamp' )

# grab the args from the argparse object
args = parser.parse_args()

# define prettier names and strip some whitespace
auth = args.auth
pod = args.pod.strip()
timestamp = args.timestamp.strip()
spreadsheet_id = args.spreadsheet_id.strip()

# convert range into a list
range = args.range.split(",")

# instantiate empty list
new_range = []

# remove all the garbage from the old list
for item in range:
  i = item.strip("[]' ")
  new_range.append(i)

# reset range var to the new data
range = new_range

# the command line can only pass strings, convert string to dict
# dict object expected by service object
json_auth = json.loads(auth)

try:
  # define requested scope, required by oauth, we're just looking at sheets here
  scopes = ["https://www.googleapis.com/auth/spreadsheets"]

  # build oauth credential object
  credentials = service_account.Credentials.from_service_account_info(json_auth, scopes=scopes)
  
  # define the service you wish to access
  service = discovery.build('sheets', 'v4', credentials=credentials)

  # grab the spreadsheet data and stor it in a var
  for sheet in range:
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet).execute()

  # define your header rows and data rows
  row_headers = result.get('values')[0]
  data_rows = result.get('values')[1:]

  # write the data to a CSV for parsing
  with open(pod + '-' + timestamp + '.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(row_headers)
    for line in data_rows:
      write.writerow(line)
  

# if it blows up, tell us why
except errors.HttpError as e:
  if e.resp.status == 403:
    print('HTTP_403 Error The service account does not have have permission to the requested document')
    
except OSError as e:
  print(e)
