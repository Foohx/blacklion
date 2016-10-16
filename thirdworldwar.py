# coding: utf-8
import requests
import re
from lxml import html

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