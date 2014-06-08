#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import os
import time
import json
import requests
import soundcloud
from connections import *
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#--------------------------Connection To Pandora API-----------------

os.remove('music.txt') if os.path.exists('music.txt') else None

StartTime = int(time.time()) #Start Time of the API in Unix timestamp format

partnerId, partnerAuthToken, syncTime = PartnerLogin()  #First Step of Login to get partnerId, partnerAuthToken and Decrypted syncTime
#print "\npartnerId = " +partnerId
#print "\npartnerAuthToken = " +partnerAuthToken
#print "\nsyncTime Decrypted = %s " %syncTime


syncTime = TimeSync(syncTime, StartTime) #Synchronized time if available. Calculation: auth.partnerLogin.syncTime + (currentClientTime - clientStartTime)
#print "\nsyncTime + (currentClientTime - clientStartTime)= %s "  %syncTime


userId, userAuthToken = UserLogin(partnerId, partnerAuthToken, syncTime) #2 Step login with pandora credential + partnerId, partnerAuthToken and syncTime
#print "\nuserId = " +userId
#print "\nuserAuthToken = + " +userAuthToken

#-----------------------Creation of the Station and retrieve music--------
while True:
    try: 
        music = raw_input("\n\nPlease enter the Artist or Track you would like to get simmilar song : ") #Ask for the Artist or music
        syncTime = TimeSync(syncTime, StartTime)
        musicToken = MusicSearch(partnerId, userAuthToken, userId, syncTime, music) #Request to find the musicToken
	break
    except IndexError:
	print "Oops!  It seems like Pandora didn't find your Artist.  Try again..."

number = int(raw_input("\nHow many song would you like to retrieve ? : ")) #number of song to retrieve

for i in range(number/4): #The number is divided by 4 because it retrive song by 4 for each request

    print "\nBundle of sounds number #%s " %i    

    syncTime = TimeSync(syncTime, StartTime)
    stationToken = CreateStation(partnerId, userAuthToken, userId, syncTime, musicToken) #Generate station with musicToken and retrieve stationToken

    try:
        syncTime = TimeSync(syncTime, StartTime)
        GetPlaylist(partnerId, userAuthToken, userId, syncTime, stationToken) #With stationToken connect to station, print playlist song and savit it to file
    except KeyError:
	print "Oops!  Pandora have been overwhelmed, try to set a longer sleep time next time.  Processing playlist creation on SoundCloud..."
        time.sleep(3)
	break
	
Duplicate(music) #Remove duplicate song

#--------------------------SoundCloud Part------------------------------
musics  = []
choices = {}
flag = 0
num = 0
match = 0

# create client object with app and user credentials
client = soundcloud.Client(client_id='YOUR_CLIENT_ID',
                           client_secret='YOUR_CLIENT_SECRET',
                           username='YOUR_USERNAME',
                           password='YOUR_PASSWORD')

# print authenticated user's username
print client.get('/me').username
 
 
with open(music, "r") as f: #Open the file with generated song by Pandora API
    for line in f:
        num += 1 #Count the number of all song
        choices = {}
        try:
            tracks = client.get('/tracks', q= line, limit=20) #Search track based on file and print the frist 200 result
        except requests.HTTPError:
            tracks = client.get('/tracks', q= line, limit=20)

	tracks = client.get('/tracks', q= line, limit=20) #Search track based on file and print the frist 20 result
        for track in tracks: #for earch song in all songs
            if fuzz.ratio(line, (track.user['username'] +" - "+ track.title)) >= 85: #if the combo (user + song) match it's probably an official one
		print "\n---------- OFFICIAL ---------"
		print line
                print track.user['username'] +" - "+ track.title
		print "---------- OFFICIAL ---------\n"
                musics.append(track.id) #Add the song ID to the list
                match += 1 #Count the number of finded song
		choices = {} #Reset choices to not enter in the next condition
                break
	    else:
	        choices[track.title] = track.id #Append to dictionary the song name + id in pair key method
	while choices: #Verify if Choices contain data in order to prevent error
	    song = process.extractOne(line, choices) #select the most similar song among other
	    if song[1] >= 95: #if the chosen song similarity rate is more or equal to 95% it's probably the good one
	        print "\n" +line
	        print song[0]
	        musics.append(choices[song[0]]) #Add the song ID to the list
		match += 1 
	    break
f.close()
print "%s songs finded on %s given" %(match, num)
 
# create an array of track ids
tracks = map(lambda id: dict(id=id), musics) #Convert the list of track ID into soundcloud import format

# get playlists 
playlists = client.get('/me/playlists') 
for playlist in playlists:
    if music == playlist.title: #Check if the playlist already exist
        flag = 1 #If already exist put the flag at 1
        # add tracks to playlist
        client.put(playlist.uri, playlist={'tracks': tracks})
        break
 
if flag == 0: #If the flag is at 0 that's mean the playlist didn't exist yet
    # create the playlist and add tracks
    client.post('/playlists', playlist={'title': music, 'sharing': 'public', 'tracks': tracks})
 
print "Congratz! Your have now %s new songs in your playlist %s on soundcloud" %(match, music)

