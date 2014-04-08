#!/usr/bin/python
"""
VECLabs Namecoin Hashrate Data Generator
Author: Jeremy Rand AKA biolizard89, Viral Electron Chaos Laboratories
"""

import json
import requests
import argparse
import ConfigParser
import os
import operator
from datetime import datetime, date, time

parser = argparse.ArgumentParser(description='VECLabs Namecoin Hashrate Data Generator')

parser.add_argument('configfile', help='Configuration File', 
                    metavar='Config.conf')

args = parser.parse_args()

config = ConfigParser.ConfigParser()

config.read(args.configfile)

btcheight = 0
nmcheight = 0
pooldata = {}
poolblocks = {}
nmcpercentage = {}
btchashrate = 0
nmchashrate = 0
nmcother = 100

# get BTC height
url = 'https://blockchain.info/q/getblockcount'
params = dict()
resp = requests.get(url=url, params=params)
data = json.loads(resp.content.decode('unicode-escape'))
print 'BTC block count:', str(data)
btcheight = data

# get BTC next difficulty
url = 'http://dot-bit.org/tools/difficulty_bitcoin.txt'
params = dict()
resp = requests.get(url=url, params=params)
rawpage = resp.content.decode()
btchashrate = json.loads(rawpage)
print 'BTC next difficulty:', str(btchashrate)

# get NMC next difficulty
url = 'http://dot-bit.org/tools/difficulty_namecoin_estimate.txt'
params = dict()
resp = requests.get(url=url, params=params)
rawpage = resp.content.decode()
nmchashrate = json.loads(rawpage)
print 'NMC next difficulty:', str(nmchashrate)

for poolname in config.sections():
    
    if str(poolname) == 'DEFAULT':
        continue
    
    #print(poolname)
    
    url = 'https://blockchain.info/blocks/' + poolname
    
    params = dict(format='json')
    
    resp = requests.get(url=url, params=params)
    
    data = json.loads(resp.content.decode('unicode-escape'))
    
    #print(str(data))
    
    pooldata[poolname] = data
    
    poolblocks[poolname] = 0
    
    for block in pooldata[poolname]['blocks']:
        
        if(block['height'] > btcheight - 100):
            poolblocks[poolname] = poolblocks[poolname] + 1
    
    print poolname, 'had', poolblocks[poolname], '% of BTC hashrate in last 100 blocks.'
    
    nmcpercentage[poolname] = max(poolblocks[poolname] * btchashrate / nmchashrate , 0)
    
    nmcother = max(nmcother - nmcpercentage[poolname], 0)
    
    print poolname, 'has', nmcpercentage[poolname], '% of NMC hashrate.'

sorted_nmcpercentage = sorted(nmcpercentage.items(), key=lambda x: x[1], reverse=True)

sorted_nmcpercentage.append(["Other", nmcother])

print "Other:", nmcother, "% of NMC hashrate."

json_out = open(config.get('DEFAULT','output'), 'w')

json.dump({"data":sorted_nmcpercentage,"last-modified":str(datetime.now()),"data-sources":"VECLabs.net, Blockchain.info, Dot-Bit.org"}, json_out)
