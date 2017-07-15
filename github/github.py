#!/usr/bin/env python

'''
Unicorn Github provider
Sends some github stats to a Unicorn Server
See https://github.com/actuino/unicorn-display/tree/master/server
'''

import os
import json
import requests

# The socker server Hostname
DISPLAY_SERVER_HOST = 'localhost'
if 'DISPLAY_SERVER_HOST' in os.environ:
    DISPLAY_SERVER_HOST = os.environ['DISPLAY_SERVER_HOST']
    
# The socker server Port
DISPLAY_SERVER_PORT = 80
if 'DISPLAY_SERVER_PORT' in os.environ:
    DISPLAY_SERVER_PORT = os.environ['DISPLAY_SERVER_PORT']

# What to watch ? cf https://developer.github.com/v3/#current-version
# could be /repo/user/repo_name (just a repo)
# or /users/actuino/repos (all repos from a user)
TO_WATCH = '/repos/actuino/unicorn-display'
if 'TO_WATCH' in os.environ:
    TO_WATCH = os.environ['TO_WATCH']

print "Watching",TO_WATCH,"sending to",DISPLAY_SERVER_HOST,DISPLAY_SERVER_PORT

def get_stats():
    # TODO: change parse method according to url structure
    url = 'https://api.github.com'+TO_WATCH
    r = requests.get(url,headers={"Accept" : "application/vnd.github.v3+json"}).json()
    filtered = {key: r[key] for key in ['stargazers_count','watchers_count','forks_count','open_issues_count','subscribers_count'] }
    return filtered

def display_binary(payload,value, row, color,background=[0,0,0]):
	binary_str = "{0:8b}".format(value)
	for x in range(0, 8):
		if binary_str[x] == '1':
			payload[row][x]=color
		else:
			payload[row][x]=background

def build_screen(stats):
    # Buffer that represents the display
    payload = [[0 for x in range(8)] for y in range(8)] 
    # stars = Yellow ?
    display_binary(payload,stats['stargazers_count'], 0, [235,235,20],[20,20,20]) 
    # watchers = green
    display_binary(payload,stats['watchers_count'], 1, [20,235,20],[20,20,20]) 
    # forks = blue
    display_binary(payload,stats['forks_count'], 2, [20,20,235],[20,20,20]) 
    # issues = red on green background
    #display_binary(payload,stats['open_issues_count'], 3, [235,20,20],[110,110,110])
    #stats['open_issues_count']=7
    display_binary(payload,stats['open_issues_count'], 3, [235,20,20],[20,110,20]) 
    return payload
    
def run_it():
    stats = get_stats()
    print stats
    payload = build_screen(stats)
    #print payload
    r = requests.post('http://'+DISPLAY_SERVER_HOST+':'+str(DISPLAY_SERVER_PORT)+'/display/', json={"Type" : "Static", "Channel" : "Github","Payload" : payload})
    print r.status_code
    
run_it()