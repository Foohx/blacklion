# coding: utf-8
import requests
import re
from lxml import html
from scrapy.selector import Selector

class ThirdWorldWar:

    def __init__(self, username, password, server):
        self.account = {
            'email': username,
            'pass': password,
            'serveur': int(server),
            'connexion': ''
        }
        self.s = requests.session()

    def rLogin(self):
        r = self.s.post('http://www.3gm.fr/index.php', data=self.account)
        r = self.s.get('http://www.3gm.fr/game/index.php')
        return self.isLogged()

    def rLogout(self):
        r = self.s.get('http://www.3gm.fr/index.php?action=deco')
        return True if not self.isLogged() else False

    def rThis(self, url):
        r = self.s.get(url)
        return r

    def rSendMessageToServer(self, message, token=False):
        r = self.s.get('http://www.3gm.fr/game/tchat.php')
        if token == False:
            b, token = self.getToken(r.content)
            if not b:
                return False
        r = self.s.post('http://www.3gm.fr/game/tchat.php', data={
            'pseudo': self.account['email'],
            'tk': token,
            'message': message,
        })
        return True

    def rSendMessageToAlliance(self, message):
        r = self.s.get('http://www.3gm.fr/game/my_ally.php')
        b, token = self.getToken(r.content)
        print(token)
        if not b:
            return False
        r = self.s.post('http://www.3gm.fr/game/my_ally.php', data={
            'pseudo': self.account['email'],
            'tk': token,
            'message': message,
        })
        return True

    def rSendMessageToUser(self, message, user):
        r = self.s.post('http://www.3gm.fr/game/modules/ajax/ajax_messagerie.php', data={
            'correspondant_post_new': user,
            'message_post_new': message,
            'id_destinataire': "",
        })
        # print(r.content)
        return True

    def getBuildings(self):
        buildings = []
        pages = ['build.php', 'production.php', 'army.php']
        for page in pages:
            r = self.s.get('http://www.3gm.fr/game/'+page)
            t = html.fromstring(r.content)
            buildName = t.xpath('//div[@class="build_top_titre"]/text()')
            buildLevl = t.xpath('//div[@class="build_top_niveau"]/span/text()')
            buildAble = t.xpath('//div[@class="build_content"]/div/a/@href')
            for name, lvl in zip(buildName, buildLevl):
                can_build = False
                if any(name in links for links in buildAble):
                    can_build = True
                buildings.insert(-1, {
                    'name': name,
                    'level': lvl,
                    'available': can_build,
                    'page': page
                })
        return buildings

    def getTroopsAvailable(self):
        r = self.s.get('http://www.3gm.fr/game/mission.php')
        t = html.fromstring(r.content)
        trpName = t.xpath('//div[@class="rapport_th"]/text()')
        trpNumber = t.xpath('//div[@class="rapport_td"]/text()')
        for i in range(0,3): trpName.pop(0)
        troops = []
        for name, qty in zip(trpName, trpNumber):
            qty = re.sub('[.]', '', qty)
            troops.insert({
                'name': name,
                'qty': qty
            })
        return troops

    def isLogged(self):
        r = self.s.get('http://www.3gm.fr/game/index.php')
        tree = html.fromstring(r.content)
        nav = tree.xpath('//div[@id="gauche"]/div[@class="menu"]/a/@href')
        if len(nav) == 0 or '../index.php?action=deco' not in nav:
            return False
        return True

    def getToken(self, html=False):
        if not html:
            r = self.s.get('http://www.3gm.fr/game/index.php')
            html = r.content
        expr = [
            '&tk=([a-z0-9]+)',
            'tk=([a-z0-9]+)',
            "<input type=hidden value='([a-z0-9]+)' name='tk' \/>",
            "<input type='hidden' name='tk' value='([a-z0-9]+)'/>",
            "<input type=\"hidden\" name=\"tk\" value='([a-z0-9]+)' \/>"
        ]
        token = None
        for e in expr:
            m = re.search(e, html)
            if m != None:
                token = m.group(1)
                break
        if token == None:
            return False, None
        return True, token
