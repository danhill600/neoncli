#!/usr/bin/evn python3
import requests
import json
import datetime


def get_apikey():
    f = open("api_key.txt",'r')
    lines = f.read().splitlines()
    apikey = lines[0]
    instance = lines[1]
    return apikey, instance

def get_sesh(apikey, instance):
    """gets a NeonCRM session ID for an instance."""
    url = "https://api.neoncrm.com/neonws/services/api/common/login?login.apiKey=" + apikey + "&login.orgid=" + instance
    ret = requests.get(url)
    respdict = json.loads(ret.text)
    sessionid = respdict['loginResponse']['userSessionId']
    return sessionid

def get_asrs_list_by_keyword(sessionid):
    """Get account search results list."""
    keywordresp = input("Please enter keyword: ")
    if keywordresp == 'q':
        exit()
    else:
        keywordurl = 'https://api.neoncrm.com/neonws/services/api/account/listAccountsByKeywordSearch?userSessionId=' + sessionid + '&page.pageSize=100&userType=Individual&keyword=' + keywordresp
        keywordret = requests.get(keywordurl)
        keyworddict = json.loads(keywordret.text)
        asrslist = keyworddict['listAccountsByKeywordSearchResponse']['accountSearchResults']['accountSearchResult']
        return asrslist

def print_memberships(sessionid, selection_acct):
    mem_url = "https://api.neoncrm.com/neonws/services/api/membership/listMembershipHistory?userSessionId=" + sessionid + "&accountId=" + str(selection_acct)
    mem_ret = requests.get(mem_url)
    mem_dict = json.loads(mem_ret.text)

    mem_list = mem_dict['listMembershipHistoryResponse']['membershipResults']['membershipResult']
    return mem_list

def add_donation(sessionid, selection_acct, selection_fn):
    nowdate = datetime.datetime.now()
    don_url = "https://api.neoncrm.com/neonws/services/api/donation/createDonation?responseType=json&userSessionId=" + sessionid + "&donation.accountId=" + str(selection_acct) + "&donation.amount=50&Payment.amount=50&donation.date=" + str(nowdate)[:10] + "&Payment.tenderType.id=3&donation.campaign.id=73&donation.purpose.id=1&donation.fund.id=1&source.id=1"
    requests.post(don_url)

    print("A new 50 dollar donation by check was made on " + selection_fn + "'s account.")

def get_acct_from_list(asrslist, sessionid):
    resultcount = 0
    for asr in asrslist:
        print(str(resultcount) + "\t" +
              str(asr['accountId']) + "\t" +
              asr['firstName'] + " " +
              asr['lastName'])
        resultcount += 1

    print(str(resultcount) + " accounts match the keyword.")
    selection = input("select account: ")
    if selection == 'q':
        exit()
    else:
        selection_acct = asrslist[int(selection)]['accountId']
        selection_fn = asrslist[int(selection)]['firstName']
        selection_ln = asrslist[int(selection)]['lastName']
        print("\n")
        print("You selected account #" + str(selection_acct))
        print("First Name: " + selection_fn)
        print("Last Name: " + selection_ln)
        print("\n")
        return selection_acct, selection_fn, selection_ln


def get_memberships_on_acct(sessionid, selection_acct, selection_fn, selection_ln):
    mem_list = print_memberships(sessionid, selection_acct)
    mem_count = 0

    bigdate = datetime.datetime(1900,1,1)

    if not mem_list:
        print(selection_fn + " " + selection_ln + " is not now, nor has ever been," +
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

def show_menu(selection_acct, selection_fn, selection_ln, sessionid):
    print("Make a selection for #" + str(selection_acct) + " " +
        selection_fn + " " + selection_ln)

    #menu_selection ==''
    #while menu_selction not in ['a','m','s','q']:

    print("a) Add a 50 dollar test donation to the account.")
    print("m) get membership info")
    print("s) search by new keyword")
    print("q) quit")
    print("----------------------------------------------")
    menu_selection = input("Enter your selection: ")

    if menu_selection == 'a':
        add_donation(sessionid, selection_acct, selection_fn)
    elif menu_selection == 'm':
        get_memberships_on_acct(sessionid, selection_acct, selection_fn, selection_ln)
    elif menu_selection == 's':
        pass
    elif menu_selection == 'q':
        exit()
