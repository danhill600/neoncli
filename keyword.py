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

asrslist = nc.get_asrs_list(sessionid)

resultcount = 0
for asr in asrslist:
    print(str(resultcount) + "\t" +
          str(asr['accountId']) + "\t" +
          asr['firstName'] + " " +
          asr['lastName'])
    resultcount += 1

print(str(resultcount) + " accounts match the keyword.")
selection = input("select account: ")
selection_acct = asrslist[int(selection)]['accountId']
selection_fn = asrslist[int(selection)]['firstName']
selection_ln = asrslist[int(selection)]['lastName']
print("You selected account #" + str(selection_acct))
print("\n")
print("First Name: " + selection_fn)
print("Last Name: " + selection_ln)

mem_list = nc.print_memberships(sessionid, selection_acct)
mem_count = 0

bigdate = datetime.datetime(1900,1,1)

if not mem_list:
    print(selection_fn + " " + selection_ln + " is not now nor ever has been" +
          " a member.")
else:
    print("Membership History:")
    print("---------------------------------------------------------")
    print("NAME" + "\t" + "\t" + "\t" + "EXP_DATE" + "\t" + "TYPE" + "\t" +  "STATUS")
    for mem in mem_list:
        print(str(mem['membershipName']) + "\t" +
              str(mem['termEndDate'])[:10] + "\t" + mem['enrollmentType'] +
                  "\t" + mem['status'])
        thisdate = datetime.datetime.strptime(mem['termEndDate'][:10],"%Y-%m-%d")
        if thisdate > bigdate:
            bigdate = thisdate

    print("---------------------------------------------------------")

    print(bigdate)
    if bigdate > datetime.datetime.now():
        print(selection_fn + " " + "is a current member.")
    else:
        print(selection_fn + "'s membership has lapsed.")



#logging out
logout = requests.get('https://api.neoncrm.com/neonws/services/api/common/logout?userSessionId=' + sessionid)
logoutDict = json.loads(logout.text)
message = logoutDict['logoutResponse']['responseMessage']
print(message)
