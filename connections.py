#!/usr/bin/python
 
import json
import requests
from blowfish import *
from keys import *
import time


def PartnerLogin():
    url = "https://tuner.pandora.com/services/json/"
    parameter = {"method" : 'auth.partnerLogin'}
    values = {
    	    "username": "android",
            "password": "AC7IBG09A3DTSYM4R41UJWL07VLN8JI7",
            "deviceModel": "android-generic",
            "version": "5"
             }

    r = requests.post(url, params = parameter, data = json.dumps(values))
    r = r.json()
    syncTime = int(PandoraDecrypt(r["result"]['syncTime'])[4:14])
    return (r["result"]["partnerId"], r["result"]["partnerAuthToken"], syncTime)


def TimeSync(syncTime, StartTime):
    ts = int(time.time())
    return syncTime + (ts - StartTime)


def UserLogin(partnerId, partnerAuthToken, syncTime):
    url = "https://tuner.pandora.com/services/json/"
    parameter = {"method" : 'auth.userLogin', "partner_id" : partnerId, "auth_token" : partnerAuthToken}
    values = {
    "loginType": "user",
    "username": "username@example.com",
    "password": "password",
    "partnerAuthToken": partnerAuthToken,
    "includeAdAttributes":True,
    "syncTime": syncTime
	     }
    data = json.dumps(values)
    data = PandoraEncrypt(data)
    r = requests.post(url, params = parameter, data = data)
    r = r.json()
    return (r["result"]["userId"], r["result"]["userAuthToken"]) 


def MusicSearch(partnerId, userAuthToken, userId, syncTime, music):
    url = "http://tuner.pandora.com/services/json/"
    parameter = {"method" : 'music.search', "partner_id" : partnerId, "auth_token" : userAuthToken, "user_id" : userId} 
    values = {
    "searchText": music,
    "userAuthToken": userAuthToken,
    "syncTime": syncTime
	     }
    data = json.dumps(values)
    data = PandoraEncrypt(data)
    r = requests.post(url, params = parameter, data = data)
    r = r.json()
    try:
	return r["result"]['songs'][0]['musicToken']
    except IndexError:
	return r["result"]['artists'][0]['musicToken']

def CreateStation(partnerId, userAuthToken, userId, syncTime, musicToken):
    url = "http://tuner.pandora.com/services/json/"
    parameter = {"method" : 'station.createStation', "partner_id" : partnerId, "auth_token" : userAuthToken, "user_id" : userId}
    values = {
    "musicToken": musicToken,
    "userAuthToken": userAuthToken,
    "syncTime": syncTime
             }
    data = json.dumps(values)
    data = PandoraEncrypt(data)
    r = requests.post(url, params = parameter, data = data)
    r = r.json()
    return r["result"]["stationToken"]


def GetPlaylist(partnerId, userAuthToken, userId, syncTime, stationToken):
    url = "https://tuner.pandora.com/services/json/"
    parameter = {"method" : 'station.getPlaylist', "partner_id" : partnerId, "auth_token" : userAuthToken, "user_id" : userId}
    values = {
    "stationToken": stationToken,
    "userAuthToken": userAuthToken,
    "syncTime": syncTime
             }
    data = json.dumps(values)
    data = PandoraEncrypt(data)
    r = requests.post(url, params = parameter, data = data)
    r = r.json()

    with open('music.txt', 'a') as f:
        for i in range(len(r["result"]["items"])-1):
	    f.write(r["result"]["items"][i]['artistName'].encode('utf-8') + " - ")
	    f.write(r["result"]["items"][i]['songName'].encode('utf-8') +"\n")
            print r["result"]["items"][i]['artistName'],
            print r["result"]["items"][i]['songName']  
        f.close() 
       
    time.sleep(20)

def Duplicate(music):
    junk = 0
    lines_seen = set() # holds lines already seen
    outfile = open(music, "w")
    for line in open('music.txt', "r"):
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
	else:
	    junk += 1
    print "\n%s duplicate songs removed " %junk
    outfile.close()
