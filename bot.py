# coding: utf-8
import time
import random
from jsondb.db import Database
from tinydb import TinyDB, Query, where
from colorama import init, Fore, Back, Style
from thirdworldwar import *

class Bot:
    # Constants
    CONST_SERVERS = {1:"TERRA", 2: "ANDHERRA", 3: "DUNDHA"}

    # Variables
    _groupID = -1
    _actionLevel = None
    _pauseTimestamp = 0
    account = None
    db = {}
    isLogged = False

    def __init__(self, u, p, s, gid):
        self._groupID = gid
        self.loadDatabases()
        self.account = ThirdWorldWar(u, p, s)
        self.isLogged = self.account.rLogin()
        self.log('+' if self.isLogged else '-',
            "Login as \""+ self.CONST_SERVERS[s] +"/"+ u +"\"", False)
        self._actionLevel = self._getGroupLevel()
        # self.setPause()

    def __del__(self):
        self.isLogged = False if self.account.rLogout() else True
        self.log('-' if self.isLogged else '+',
            "Disconnect from \""+ self.CONST_SERVERS[self.account.account['serveur']] +"/"+ self.account.account['email'] +"\"", False)

    def hello(self):
        if not self._isPauseFinished():
            return False
        self.log('?', "Selecting \""+ self.CONST_SERVERS[self.account.account['serveur']] +"/"+ self.account.account['email'] +"\"", True)
        self.log('?', "Group \""+self._getGroupData(self._groupID)['name']+"\" [ID:"+str(self._groupID)+"] / Level "+str(self._actionLevel))

    def loadDatabases(self):
        self.db['groups'] = Database("cache/db/groups.json")
        self.db['maps'] = TinyDB('cache/db/maps.json')
        self.db['ranks'] = TinyDB('cache/db/ranks.json', sort_keys=True, indent=4)

    def setPause(self):
        if time.time() >= self._pauseTimestamp:
            self._pauseTimestamp = time.time() + (random.randint(1,30)*60)

    def _isPauseFinished(self):
        return True if time.time() >= self._pauseTimestamp else False

    def functions(self):
        if not self._isPauseFinished():
            return False
        try:
            group = self._getGroupData(self._groupID)
            if group != None and "functions" in group:
                for f in group['functions']:
                    self.log("?", "Function "+f+" is define in groups..")
                    userFunc = getattr(self, f)
                    self.log("!", "Calling "+f+"()...")
                    userFunc()
        except AttributeError:
            self.log("-", "Function does not exist !", True)
            pass

    def _fncChatBotAlly(self):
        messages = self.account.getChatAlliance()
        for message in messages:
            m = message['message'].split(' ')
            if (message['elasped']/60) > 12: break
            if m[0] == "!base":
                self._fncChatBotAlly_cmdBase(m)
            elif m[0] == "!who_plays":
                self._fncChatBotAlly_cmdWhoPlays(m)
            break

    def _fncChatBotAlly_cmdBase(self, m):
        if len(m) >= 2:
            self.log("+", "Receive command !base")
            pseudo = ""
            i = 1
            while i<len(m):
                pseudo = pseudo + " " + m[i]
                pseudo = pseudo.strip()
                i = i +1
            self.log("?", "Searching bases for user \"" + pseudo + "\"..")

            table = self.db['maps'].table('server_'+str(self.account.account['serveur']))
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
            self.account.rSendMessageToAlliance(rapport)
        else :
            log("-", "Receive command !base, but no args..")

    def _fncChatBotAlly_cmdWhoPlays(self, m):
        self.log("+", "Receive command !who_plays")
        table = self.db['ranks'].table('server_'+str(self.account.account['serveur']))

        # scan_date = table.get(where('id'), len(table))
        # scan_date = scan_date['scan_date']

        ranks_old = table.all()
        ranks_now = self.account.getRanking()
        self.log("?", "Searching for actives users..")
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
                        self.account.rSendMessageToAlliance(rapport)
                        rapport = ""
                    break
        rapport = rapport + "OVER !"
        self.account.rSendMessageToAlliance(rapport)

    def workers(self):
        if not self._isPauseFinished():
            return False
        self._actionLevel = self._getGroupLevel()
        self._workersActionsForBuildings()
        self._workersActionsForTechnology()
        self._workersActionsForTroops()

    def _workersActionsForBuildings(self):
        feeds = self.account.getFeeds()
        b, index = self._isIn("Buildings", feeds, "name")
        if not b: return
        if int(feeds[index]['actives']) >= int(feeds[index]['max']):
            self.log("!", "Buildings feed is full !", True)
            return
        actions = self._getGroupActionForLevel(self._actionLevel)
        if actions == None: return
        builds = self.account.getBuildings()
        for action in actions:
            kword = "entity"
            b, bIndex = self._isIn(action[kword], builds, "name")
            if not b:
                continue
            if builds[bIndex]['available'] == True and int(action['level']) > int(builds[bIndex]['level']):
                isOk = self.account.rStartBuilding(builds[bIndex]["name"])
                self.log(
                    '+' if isOk else '-',
                    "Starting building \""+builds[bIndex]["name"]+"\" (lvl:"+builds[bIndex]["level"]+"/"+str(action['level'])+")",
                    True
                )
                feeds[index]['actives'] = int(feeds[index]['actives']) +1 if isOk else int(feeds[index]['actives'])
            if int(feeds[index]['actives']) >= int(feeds[index]['max']):
                return
        return

    def _workersActionsForTechnology(self):
        actions = self._getGroupActionForLevel(self._actionLevel)
        if actions == None: return
        builds = self.account.getTechnology()
        for action in actions:
            b, bIndex = self._isIn(action['entity'], builds, "name")
            if not b:
                continue
            if int(builds[bIndex]['level']) < int(action['level']):
                if builds[bIndex]['activable']:
                    isOk = self.account.rTechActivate(action['entity'])
                    self.log('+' if isOk else "-", "Tech \""+action['entity']+"\" activated!", True)
                elif builds[bIndex]['available'] == True and not builds[bIndex]['feed']:
                    isOk = self.account.rTechStart(action['entity'])
                    checkBuilds = self.account.getTechnology()
                    cb, cbIndex = self._isIn(action['entity'], checkBuilds, "name")
                    if cb:
                        self.log('+' if isOk and checkBuilds[cbIndex]['feed'] else '-', "Starting technology \""+action['entity']+"\"", True)

    def _workersActionsForTroops(self):
        n =0



    def _getGroupData(self, gid):
        for grp in self.db['groups'].data()['groups']:
            if grp['id'] == gid:
                return grp
        return None

    def _getGroupActions(self):
        actions = []
        group = self._getGroupData(self._groupID)
        if group == None: return None
        if "actions_from" in group:
            group = self._getGroupData(group['actions_from'])
            if group == None: return None
        for action in group['actions']:
            actions.append(action)
        return actions if len(actions) >0 else None

    def _isIn(self, value, into, kword):
        count = 0
        for i in into:
            if i[kword] == value:
                return True, count
            count = count +1
        return False, None

    def _getGroupLevel(self):
        userBuilds = self.account.getBuildings()
        userBuilds = userBuilds + self.account.getTechnology()
        userBuilds = userBuilds + self.account.getTroops()
        level = 0
        while level != None:
             actions = self._getGroupActionForLevel(level)
             if actions == None: return None
             for action in actions:
                 b, index = self._isIn(action['entity'], userBuilds, 'name')
                 if not b:
                     b, index = self._isIn(action['entity'], userBuilds, 'alias')
                     if not b: return level
                 if int(userBuilds[index]['level']) < int(action['level']):
                     return level
             level = level +1

    def _getGroupActionForLevel(self, lvl):
        actionsForLevel = []
        actionsAll = self._getGroupActions()
        if actionsAll == None: return None
        for action in actionsAll:
            if action['id'] == lvl:
                actionsForLevel.append(action)
        return actionsForLevel if len(actionsForLevel) >0 else None

    def log(self, prefix, text, line=False):
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
            print c+"["+now.strftime("%Y-%m-%d %H:%M:%S")+"]["+prefix+"] "+text+e
        else :
            print "["+now.strftime("%Y-%m-%d %H:%M:%S")+"]["+c+prefix+e+"] "+text
