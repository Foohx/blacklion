# coding: utf-8
import sys
import random
from colorama import init, Fore, Back, Style
from jsondb.db import Database
from tinydb import TinyDB, Query, where
from thirdworldwar import *

if __name__ != "__main__":
    sys.exit(1)

init(autoreset=True)
dbAccounts = Database("cache/db/accounts.json")
dbGroups = Database("cache/db/groups.json")
dbMaps = TinyDB('cache/db/maps.json')
dbRanks = TinyDB('cache/db/ranks.json', sort_keys=True, indent=4)

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
                        elif 'alias' in action and action['alias'] == d['name'] and int(d['level']) >= action['level']:
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
            return True, i
    return False, []

# Send some ressources from user to each coords
# coords = [
#     {'x':165,'y':229},
#     {'x':239,'y':265},
#     {'x':155,'y':110},
#     {'x':287,'y':162},
#     {'x':230,'y':160},
#     {'x':222,'y':108},
#     {'x':111,'y':199},
#     {'x':131,'y':262},
#     {'x':238,'y':271},
#     {'x':272,'y':218}
# ]
# h = ThirdWorldWar('user', 'pass', 3)
# h.rLogin()
# for coord in coords:
#     r = h.rMission(coord['x'], coord['y'])
#     print(r, coord['x'], coord['y'])
#     time.sleep(10)
# sys.exit(0)

# # Loading and login accounts
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
    log("?", "Alive loop..", True)
    for user in users:
        log("!", "User \""+user['user'].account['email']+"\" was selected !", True)
        AP = user['user'].getBases()
        BCOUNT = 0
        TECHS = []
        for ap in AP :
            log("!", "Selected base ("+ap+") !")
            user['user'].rChangeBase(ap)
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
            if BCOUNT == 0:
                TECHS = user['techs']
                if len(user['techs']) == 0:
                    log("-", "Getting technology..")
                else :
                    log("+", "Getting technology..")
            else :
                user['techs'] = TECHS
            if 'actions' in user['group']:
                step = selectStep([user['builds'], user['techs']])
                actions = selectActions(step)
                if actions == None:
                    log("-", "User is level max ("+str(step)+") in \""+user['group']['name']+"\"")
                    continue
                else :
                    log("?", "User is level ("+str(step)+") in \""+user['group']['name']+"\"")

                # Manage buildings
                #   just for read in feed
                i = getIndexFor('Buildings', feed)
                if int(feed[i]['actives']) < int(feed[i]['max']):
                    n = int(feed[i]['actives'])
                    for action in actions:
                        b, data = isNameAvailable(action['entity'], user['builds'])
                        if b and data['available']==True and int(data['level']) < int(action['level']):
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
                # print(user['techs'])
                if len(user['techs']) > 0 and BCOUNT == 0:
                    for action in actions:
                        b, data = isNameAvailable(action['entity'], user['techs'])
                        if b and int(data['level']) < int(action['level']):
                            # print(data)
                            # is tech need to be activate ?
                            if data['activable'] == True:
                                r = user['user'].rTechActivate(data['name'])
                                if r:
                                    log('+', "Technology \""+action['entity']+"\" activated", True)
                                else :
                                    log('-', "Technology \""+action['entity']+"\" not activated", True)
                            elif data['available'] == True and not data['feed']:
                                r = user['user'].rTechStart(data['name'])
                                if r:
                                    log('+', "Starting technology \""+action['entity']+"\"", True)
                                else :
                                    log('-', "Starting technology \""+action['entity']+"\"", True)
            BCOUNT = BCOUNT +1
        if 'functions' in user['group']:
            for function in user['group']['functions']:
                if function == 'chatbot':
                    log("?", "Chatbot..", True)
                    messages = user['user'].getChatAlliance()
                    for message in messages:
                        print(message)
                        m = message['message'].split(' ')
                        if (message['elasped']/60) > 12:
                            break
                        if m[0] == "!base":
                            if len(m) >= 2:
                                log("+", "Receive command !base")
                                pseudo = ""
                                i = 1
                                while i<len(m):
                                    pseudo = pseudo + " " + m[i]
                                    pseudo = pseudo.strip()
                                    i = i +1
                                log("?", "Searching bases for user \"" + pseudo + "\"..")

                                table = dbMaps.table('server_'+str(user['user'].account['serveur']))
                                scan_date = table.get(where('id'), len(table))
                                scan_date = scan_date['scan_date']
                                bases = table.search((where('scan_date') == scan_date) & (where('user') == pseudo))

                                rapport = "Extract from " + str(scan_date) + " scan !\n\n"
                                rapport = rapport + "Wanted : @"+pseudo+"\n"
                                rapport = rapport + "---\n"
                                for base in bases:
                                    if 'x' in base and 'y' in base and 'name' in base:
                                        rapport = rapport + "- " + base['name'] + " | " + str(base['x']) + "-" + str(base['y']) + "\n"
                                rapport = rapport + "---\n"
                                rapport = rapport + "OVER !"
                                user['user'].rSendMessageToAlliance(rapport)
                            else :
                                log("-", "Receive command !base, but no args..")
                        elif m[0] == "!who_plays":
                            log("+", "Receive command !who_plays")
                            table = dbRanks.table('server_'+str(user['user'].account['serveur']))

                            # scan_date = table.get(where('id'), len(table))
                            # scan_date = scan_date['scan_date']

                            ranks_old = table.all()
                            ranks_now = user['user'].getRanking()
                            log("?", "Searching for actives users..")
                            rapport = "Active players for last 5 days :\n\n"
                            count = 0
                            for rn in ranks_now:
                                for ro in ranks_old:
                                    if rn['user'] == ro['user']:
                                        if (ro['points'] - rn['points']) != 0:
                                            count = count +1
                                            rapport = rapport + "- @" + rn['user'] + " ("+str((rn['points'] - ro['points']))+" pts)\n"
                                        if count >= 7:
                                            count = 0
                                            user['user'].rSendMessageToAlliance(rapport)
                                            rapport = ""
                                        break
                            rapport = rapport + "OVER !"
                            user['user'].rSendMessageToAlliance(rapport)

                        # if len(m) < 2:
                        #     print(m)
                        break

    pause = random.randint(1,10)
    log("?", "Waiting for "+str(pause)+" minutes..", True)
    time.sleep(60*pause)


#
# Traceback (most recent call last):
#   File "./blacklion.py", line 131, in <module>
#     messages = h.getChatAlliance()
#   File "/mnt/c/Users/Foohx/Documents/GitHub/blacklion/thirdworldwar.py", line 195, in getChatAlliance
#     r = self.s.get('http://www.3gm.fr/game/my_ally.php')
#   File "/mnt/c/Users/Foohx/Documents/GitHub/blacklion/cache/env/local/lib/python2.7/site-packages/requests/sessions.py", line 488, in get
#     return self.request('GET', url, **kwargs)
#   File "/mnt/c/Users/Foohx/Documents/GitHub/blacklion/cache/env/local/lib/python2.7/site-packages/requests/sessions.py", line 475, in request
#     resp = self.send(prep, **send_kwargs)
#   File "/mnt/c/Users/Foohx/Documents/GitHub/blacklion/cache/env/local/lib/python2.7/site-packages/requests/sessions.py", line 596, in send
#     r = adapter.send(request, **kwargs)
#   File "/mnt/c/Users/Foohx/Documents/GitHub/blacklion/cache/env/local/lib/python2.7/site-packages/requests/adapters.py", line 487, in send
#     raise ConnectionError(e, request=request)
# requests.exceptions.ConnectionError: HTTPConnectionPool(host='www.3gm.fr', port=80): Max retries exceeded with url: /game/my_ally.php (Caused by NewConnectionError('<requests.packages.urllib3.connection.HTTPConnection object at 0x7faf27a01b10>: Failed to establish a new connection: [Errno -2] Name or service not known',))
