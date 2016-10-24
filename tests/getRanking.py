import sys
from tinydb import TinyDB, Query
from thirdworldwar import *
from _account_ import *

db = TinyDB('../cache/db/ranks.json', sort_keys=True, indent=4)
table = db.table('server_'+str(server))

h = ThirdWorldWar(username, password, server)
h.rLogin()

old = table.all()
ranks = h.getRanking()
for r in ranks:
    for o in old:
        if r['user'] == o['user']:
            print(r['user'], r['points']-o['points'])
            break
