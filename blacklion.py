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

# Loading and login accounts
users = []
print("[+] Loading users :")
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
    print("[+] Working :")
    time.sleep(60)
