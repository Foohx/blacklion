# coding: utf-8
import sys
import time
import datetime
from jsondb.db import Database
from tinydb import TinyDB, Query
from thirdworldwar import *
from _account_ import *
from colorama import init, Fore, Back, Style

serverID = 2
scanDate = int(time.time())

db = TinyDB('../cache/db/maps.json', sort_keys=True, indent=4)
server = db.table('server_'+str(serverID))

def log(prefix, text, line=False):
    now = datetime.now()
    message = ""
    if prefix == '?':
        c = Fore.CYAN
    elif prefix == '+':
        c = Fore.GREEN
    elif prefix == '-':
        c = Fore.RED
    elif prefix == '!':
        c = Fore.YELLOW
    c = Style.BRIGHT + c
    e = Style.RESET_ALL + Fore.RESET
    if line:
        print c+"["+now.strftime("%Y-%m-%d %H:%M")+"]["+prefix+"] "+text+e
    else :
        print "["+now.strftime("%Y-%m-%d %H:%M")+"]["+c+prefix+e+"] "+text

dbAccounts = Database("../cache/db/accounts.json")

users = []
log('?', "Login..", True)
for user in dbAccounts.data()['users']:
    if user['server'] != serverID:
        continue
    handle = ThirdWorldWar(user['nickname'], user['password'], user['server'])
    if not handle.rLogin():
        log('-', "Login for user \""+user['nickname']+"\"", False)
        continue
    log('+', "Login for user \""+user['nickname']+"\"", False)
    users.append(handle)

log('?', "Scanning..", True)
i = 0
for x in range(100,310, 10):
    for y in range(100,310, 10):
        log('!', "Getting bases at ["+str(x)+"-"+str(y)+"] with "+users[i].account['email'])
        bases = users[0].getMap(x, y)
        for base in bases:
            base['scan_date'] = scanDate
            print(base)
            server.insert(base)
        time.sleep(2)
        r = users[i].getFeeds()
        time.sleep(1)
        if i == len(users) -1:
            i = 0
        else :
            i = i +1

log("!", "Resume data..", True)
