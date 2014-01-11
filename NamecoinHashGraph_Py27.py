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
btcdifficulty = 0
nmcdifficulty = 0

# get BTC height
url = 'https://blockchain.info/q/getblockcount'
params = dict()
resp = requests.get(url=url, params=params)
data = json.loads(resp.content.decode('unicode-escape'))
print 'BTC block count: ', str(data)
btcheight = data

# get BTC difficulty
url = 'https://blockchain.info/q/getdifficulty'
params = dict()
resp = requests.get(url=url, params=params)
data = json.loads(resp.content.decode('unicode-escape'))
print 'BTC difficulty: ', str(data)
btcdifficulty = data

# get NMC difficulty
#url = 'http://dot-bit.org/tools/namecoinCalculator.php'
url = 'http://blockchained.com/namecoin/'
params = dict()
resp = requests.get(url=url, params=params)
rawpage = resp.content.decode()
#start = rawpage.find("Current difficulty : ") + len("Current difficulty : ")
start = rawpage.find("Current difficulty: ") + len("Current difficulty: ")
end = rawpage.find(" (", start)
nmcdifficulty = json.loads(rawpage[start:end])
print 'NMC difficulty: ', str(nmcdifficulty)


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
    
    print poolname, ' had ', poolblocks[poolname], '% of BTC hashrate in last 100 blocks.'
    
    nmcpercentage[poolname] = poolblocks[poolname] * btcdifficulty / nmcdifficulty 
    
    print poolname, ' has ', nmcpercentage[poolname], '% of NMC hashrate.'

sorted_nmcpercentage = sorted(nmcpercentage.items(), key=lambda x: x[1], reverse=True)
    
json_out = open(config.get('DEFAULT','output'), 'w')

json.dump({"data":sorted_nmcpercentage,"last-modified":str(datetime.now())}, json_out)
