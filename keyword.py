#!/usr/bin/env python3
import requests
import json
import nc_functions as nc
import datetime

#this module allows the user to search a NeonCRM instance for accounts by key-
#word.  It is the first in a series of modules to provide an efficient command
#line interface for common tasks performed to troubleshoot client issues.
#Dan Hill 11/19

apikey, instance = nc.get_apikey()

#getting a sessionID

sessionid = nc.get_sesh(apikey, instance)

#searching accounts by keyword

print("Welcome to NeonCLI. Enter 'q' at any time to quit.")

while True:
    asrslist = nc.get_asrs_list_by_keyword(sessionid)
    if asrslist:
        selection_acct, selection_fn, selection_ln = nc.get_acct_from_list(asrslist, sessionid)
        nc.show_menu(selection_acct, selection_fn, selection_ln, sessionid)
    else:
        print("no results found")


#logging out
logout = requests.get('https://api.neoncrm.com/neonws/services/api/common/logout?userSessionId=' + sessionid)
logoutDict = json.loads(logout.text)
message = logoutDict['logoutResponse']['responseMessage']
print(message)
