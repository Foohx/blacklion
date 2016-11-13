# coding: utf-8
import sys
import random
from jsondb.db import Database
from colorama import init, Fore, Back, Style
from bot import *

if __name__ != "__main__":
    sys.exit(1)

init(autoreset=True)

# load accounts database
DB_ACCOUNTS = Database("cache/db/accounts.json")

bots = []
try:
    # Init bots
    for user in DB_ACCOUNTS.data()['users']:
        bot = Bot(
            user['nickname'],
            user['password'],
            user['server'],
            user['group']
        )
        if bot.isLogged:
            bots.append(bot)
        # break
    # Heartbeat
    while 1:
        for bot in bots:
            bot.hello()
            bot.functions()
            bot.workers()
            bot.setPause()
        print("Pause..")
        for i in range(0,60):
            time.sleep(1)
except KeyboardInterrupt:
    # Interrupt with Ctrl+C
    print("")
    while len(bots):
        del bots[0]
    sys.exit(0)


                # Manage Army
    #             index_troops = getIndexFor('Troops', feed)
    #             if len(user['troops']) > 0 and int(feed[index_troops]['actives']) == 0:
    #                 for action in actions:
    #                     b, data = isNameAvailable(action['entity'], user['troops'])
    #                     if b and int(data['level']) < int(action['level']):
    #                         r = user['user'].rArmyStart(action['entity'], action['level'])
    #                         if r:
    #                             log('+', "Building x"+str(action['level'])+" \""+str(action['entity'])+"\"", True)
    #                         else :
    #                             log('-', "Building x"+str(action['level'])+" \""+str(action['entity'])+"\"", True)
    #
    #
    # pause = random.randint(1,10)
    # log("?", "Waiting for "+str(pause)+" minutes..", True)
    # for it in range(0, pause):
    #     log("?", str(pause-it)+" minutes remains !", False)
    #     time.sleep(60)
    #

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
