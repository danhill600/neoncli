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

def get_asrs_list(sessionid):
    """Get account search results list."""
    keywordresp = input("Please enter keyword: ")
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
    don_url = "https://api.neoncrm.com/neonws/services/api/donation/createDonation?responseType=json&userSessionId=" + sessionid + "&donation.accountId=" + str(selection_acct) + "&donation.amount=50&Payment.amount=50&donation.date=" + str(nowdate)[:10] + "&Payment.tenderType.id=3"
    requests.post(don_url)

    print("A new 50 dollar donation by check was made on " + selection_fn + "'s account.")
