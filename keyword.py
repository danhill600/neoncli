#!/usr/bin/env python3
import requests
import json

#this module allows the user to search a NeonCRM instance for accounts by key-
#word.  It is the first in a series of modules to provide an efficient command
#line interface for common tasks performed to troubleshoot client issues.
#Dan Hill 11/19

#getting the api key and instance name from text file

f = open("api_key.txt",'r')
lines = f.read().splitlines()
apikey = lines[0]
instance = lines[1]

#getting a sessionID

url = "https://api.neoncrm.com/neonws/services/api/common/login?login.apiKey=" + apikey + "&login.orgid=" + instance

ret = requests.get(url)
respdict = json.loads(ret.text)
sessionid = respdict['loginResponse']['userSessionId']

#searching accounts by keyword

keywordresp = input("Please enter keyword: ")
keywordurl = 'https://api.neoncrm.com/neonws/services/api/account/listAccountsByKeywordSearch?userSessionId=' + sessionid + '&page.pageSize=100&userType=Individual&keyword=' + keywordresp
keywordret = requests.get(keywordurl)
keyworddict = json.loads(keywordret.text)

#heirarchy of keyworddict
#listaccountsbykeywordsearchresponce (dict)
#   operationresult
#   responseDateTime
#   accountSearchResults (dict)
#       accountSearhResult (list)
#           the actual account dict

asrslist = keyworddict['listAccountsByKeywordSearchResponse']['accountSearchResults']['accountSearchResult']

resultcount = 0
for asr in asrslist:
    print(str(asr['accountId']) + " " +
          asr['firstName'] + " " +
          asr['lastName'])
    resultcount += 1

print(str(resultcount) + " accounts match the keyword.")

#we should make a menu here to allow the user to choose from among the results.

#then once the user has chosen, we'll retrieve the individual account 
#https://developer.neoncrm.com/api/accounts/retrieve-individual-account/

#then finally once we've got the account ID from the retrieved account we'll
#query the account's membership history, see if we've got a current membership
#and output either yes a member or no not a member.  
#https://developer.neoncrm.com/api/memberships/list-membership-history/

#logging out
logout = requests.get('https://api.neoncrm.com/neonws/services/api/common/logout?userSessionId=' + sessionid)
logoutDict = json.loads(logout.text)
message = logoutDict['logoutResponse']['responseMessage']
print(message)
