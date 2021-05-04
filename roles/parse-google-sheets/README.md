parse-google-sheets
=========

Use this role to get sheet data from google sheets

Requirements
------------

This role requires the following:
1. The google api service must be enabled
2. A google service account must be created
3. The service account must have at least read access to the sheet (accomplished via sharing)
4. The json auth key that is created when the service account is created
5. The device running this role must have python 3 (if the python3 binary is not located /usr/bin then the task will need to be updated)
6. The python environment that this playbook runs in must have httplib2, json, and the google-api-python-client modules installed.

Role Variables
--------------
auth (dictionary): This is the dictionary form of the service account's auth token, convert it from json to yaml (if necessary here is a tool:https://www.json2yaml.com/).

spreadsheet_id (string): This is the id of the spreadsheet you wish to process.  This can be extracted by browsing to you spreadsheet and grabbing the string immediately following the '/d/'.  For example:

https://docs.google.com/spreadsheets/d/1ajqBvzdXnhC96PhiUgeUtUkkOC0vh05T0fd0_oYUig99/edit#gid=0

In this url the spreadsheet id is: 1ajqBvzdXnhC96PhiUgeUtUkkOC0vh05T0fd0_oYUig99

range (list): This is the sheet(s) and the range of cells you would like to select from that sheet.  Specify multiple items if you need multiple sheets.  If you just specify a sheet it will grab all cells in that sheet.


Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```
- hosts: all
  tasks:
    - name: import role
      include_role: 
        name: parse-google-sheets
```

