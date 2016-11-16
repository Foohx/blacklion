# coding: utf-8
import sys
from thirdworldwar import *
from _account_ import *

h = ThirdWorldWar(username, password, server)
h.rLogin()

r = h.getTroops()
print(r)
r = h.getTroopsAvailable()
print(r)

h.rArmyStart("Fourgons", 1)
