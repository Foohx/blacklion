# coding: utf-8
import sys
import time
import datetime
import random
from colorama import init, Fore, Back, Style
from jsondb.db import Database
from thirdworldwar import *

if __name__ != "__main__":
    sys.exit(1)

init(autoreset=True)
dbAccounts = Database("cache/db/accounts.json")
dbGroups = Database("cache/db/groups.json")

def log(prefix, text, line=False):
    now = datetime.datetime.now()
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

def selectGroup(gid):
    for group in dbGroups.data()['groups']:
        if group['id'] == gid:
            return group
    return None

def selectActions(aid):
    actions = []
    for action in group['actions']:
        if action['id'] == aid:
            actions.append(action)
    if len(actions) == 0:
        return None
    return actions

def selectStep(datas):
    step = 0
    i = 0
    b = True
    while b != None:
        b = selectActions(i)
        if b != None:
            aMax = len(b)
            aCnt = 0
            for action in b:
                # Compare action ID with user building
                for data in datas:
                    for d in data:
                        if action['entity'] == d['name'] and int(d['level']) >= action['level']:
                            aCnt = aCnt +1
            if aCnt == aMax:
                step = step +1
            else:
                break
        i = i +1
    return step

def getIndexFor(search, into):
    count = 0
    for i in into:
        if i['name'] == search:
            break
        count = count +1
    return count

def isNameAvailable(search, into):
    for i in into:
        if i['name'] == search:
            return i['available'], i
    return False, []

# Loading and login accounts
users = []
log("?", "Loading users..", True)
for user in dbAccounts.data()['users']:
    handle = ThirdWorldWar(user['nickname'], user['password'], user['server'])
    if not handle.rLogin():
        log('-', "Login for user \""+user['email']+"\"", False)
        continue
    log('+', "Login for user \""+user['email']+"\"", False)
    group = selectGroup(user['group'])
    if group == None:
        log('-', "Group "+str(user['group'])+" does not exist !", False)
        continue
    log("?", "Group \""+group['name']+"\" selected", False)
    users.append({
        'user': handle,
        'group': group
    })

# Startup life loop
while len(users) > 0:
    log("?", "Starting loop life..", True)
    for user in users:
        log("!", "User \""+user['user'].account['email']+"\" was selected !", True)
        feed = user['user'].getFeeds()
        if len(feed) == 0:
            log("-", "Getting feed !", False)
            continue
        log("+", "Getting feed !", False)
        user['builds'] = user['user'].getBuildings()
        if len(user['builds']) == 0:
            log("-", "Getting buildings..")
        else:
            log("+", "Getting buildings..")
        user['techs'] = user['user'].getTechnology()
        if len(user['techs']) == 0:
            log("-", "Getting technology..")
        else :
            log("+", "Getting technology..")
        step = selectStep([user['builds'], user['techs']])
        actions = selectActions(step)
        if actions == None:
            log("-", "User is level max ("+str(step)+") in \""+user['group']['name']+"\"")
            continue
        else :
            log("?", "User is level ("+str(step)+") in \""+user['group']['name']+"\"")

        # Manage buildings
        i = getIndexFor('Buildings', feed)
        if int(feed[i]['actives']) < int(feed[i]['max']):
            n = int(feed[i]['actives'])
            for action in actions:
                b, data = isNameAvailable(action['entity'], user['builds'])
                if b and int(data['level']) < int(action['level']):
                    r = user['user'].rStartBuilding(action['entity'])
                    if r:
                        log('+', "Starting building \""+action['entity']+"\"", True)
                        n = n +1
                    else:
                        log("-", "Starting building \""+action['entity']+"\"", True)
                    if n == int(feed[i]['max']):
                        break
        else :
            log("-", "Building feed is full !", True)

        # Manage techs
        

    pause = random.randint(1,10)
    log("?", "Waiting for "+str(pause)+" minutes..", True)
    time.sleep(60*pause)
