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

    def rTuto(self):
        r = self.s.get('http://www.3gm.fr/game/production.php?tuto=8')

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
                in_feed = False
                if any(name in links for links in buildAble):
                    can_build = True
                    for link in buildAble:
                        if name in link:
                            m = re.search("ub=", link)
                            if m != None:
                                can_build = False
                                in_feed = True
                buildings.insert(-1, {
                    'name': name,
                    'level': lvl,
                    'available': can_build,
                    'feed': in_feed,
                    'page': page
                })
        return buildings

    def getTroops(self):
        r = self.s.get('http://www.3gm.fr/game/troops.php')
        t = html.fromstring(r.content)
        trpName = t.xpath('//div[@class="build_top_titre"]/text()')
        trpNumber = t.xpath('//div[@class="build_top_niveau"]/span/text()')
        troops = []
        for name, qty in zip(trpName, trpNumber):
            qty = re.sub('[.]', '', qty)
            troops.insert(-1, {
                'name': name,
                'qty': int(qty)
            })
        return troops

    def getTroopsAvailable(self):
        r = self.s.get('http://www.3gm.fr/game/mission.php')
        t = html.fromstring(r.content)
        trpName = t.xpath('//div[@class="rapport_th"]/text()')
        trpNumber = t.xpath('//div[@class="rapport_td"]/text()')
        for i in range(0,3): trpName.pop(0)
        troops = []
        for name, qty in zip(trpName, trpNumber):
            qty = re.sub('[.]', '', qty)
            troops.insert(-1, {
                'name': name,
                'qty': int(qty)
            })
        return troops

    def getDefenses(self):
        r = self.s.get('http://www.3gm.fr/game/defense.php')
        t = html.fromstring(r.content)
        defName = t.xpath('//div[@class="build_top_titre"]/text()')
        defNumber = t.xpath('//div[@class="build_top_niveau"]/span/text()')
        defenses = []
        for name, qty in zip(defName, defNumber):
            qty = re.sub('[.]', '', qty)
            defenses.insert(-1, {
                'name': name,
                'qty': int(qty)
            })
        return defenses

    def getFeeds(self):
        r = self.s.get('http://www.3gm.fr/game/index.php')
        t = html.fromstring(r.content)
        feeds = [
            {'name': 'Buildings', 'keywords': 'en construction'},
            {'name': 'Units', 'keywords': 'Unit'},
            {'name': 'Technologies', 'keywords': 'Technologies en recherche'},
            {'name': 'Defenses', 'keywords': 'fenses en cours de cr'},
            {'name': 'Troops', 'keywords': 'Mouvements de troupes'}
        ]
        for feed in feeds:
            qty_value = t.xpath('//div[@class="centre_content_title" and contains(text(),"'+feed['keywords']+'")]/span/text()')
            if len(qty_value) > 0:
                qty = qty_value[0].split('/')
                qty = [int(qty[0]), int(qty[1])]
            else : qty = [0,0]
            feed.pop('keywords', None)
            feed['actives'] = qty[0]
            feed['max'] = qty[1]
        return feeds

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
