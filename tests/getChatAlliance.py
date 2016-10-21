# coding: utf-8
import sys
import time
from thirdworldwar import *
from _account_ import *

h = ThirdWorldWar(username, password, server)
h.rLogin()

pause = 5
while 1:
    chat = h.getChatAlliance()
    for c in chat:
        age = c['elasped']/60
        if age < 11 and c['message'] == '!ping':
            h.rSendMessageToAlliance('p\nong')
        break
    time.sleep(60*pause)
