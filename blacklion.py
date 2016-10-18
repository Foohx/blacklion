# coding: utf-8
import sys
import time
from jsondb.db import Database
from thirdworldwar import *

if __name__ != "__main__":
    sys.exit(1)

dbAccounts = Database("cache/db/accounts.json")
dbGroups = Database("cache/db/groups.json")

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
print("[+] Loading users..")
for user in dbAccounts.data()['users']:
    handle = ThirdWorldWar(user['nickname'], user['password'], user['server'])
    if not handle.rLogin():
        print("[N] Login for user \""+user['email']+"\"")
        continue
    print("[Y] Login for user \""+user['email']+"\"")
    group = selectGroup(user['group'])
    if group == None:
        print("[N] Group "+str(user['group'])+" does not exist !")
        continue
    print("[Y] Group \""+group['name']+"\" selected")
    users.append({
        'user': handle,
        'group': group
    })

# Startup life loop
while len(users) > 0:
    print("[+] Loop life !")
    for user in users:
        print("[I] User \""+user['user'].account['email']+"\" was selected")
        feed = user['user'].getFeeds()
        if len(feed) == 0: continue
        user['builds'] = user['user'].getBuildings()
        user['techs'] = user['user'].getTechnology()
        step = selectStep([user['builds'], user['techs']])
        actions = selectActions(step)
        if actions == None:
            print("[I] User is level ("+str(step)+") max")
            continue
        else :
            print("[I] User is level ("+str(step)+")")
        i = getIndexFor('Buildings', feed)
        if int(feed[i]['actives']) < int(feed[i]['max']):
            n = int(feed[i]['actives'])
            for action in actions:
                b, data = isNameAvailable(action['entity'], user['builds'])
                if b and int(data['level']) < int(action['level']):
                    r = user['user'].rStartBuilding(action['entity'])
                    if r:
                        print("[Y] Starting \""+action['entity']+"\"")
                        n = n +1
                    else:
                        print("[N] Starting \""+action['entity']+"\"")
                    if n == int(feed[i]['max']):
                        break
        else :
            print("[-] Building feed is full !")


    time.sleep(60)
