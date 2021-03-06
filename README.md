# BlackLion

BlackLion est un bot pour le jeu en ligne [3GM](http://www.3gm.fr/) (3ème Guerre Mondiale). Il vous permet ainsi de jouer un ou plusieurs comptes sans être en permanence devant votre ordinateur.

* Gestion multi-compte
* Gestion multi-serveur
* Construction des bâtiments
* Lancement des recherches
* Activation des recherches
* Construction des troupes (En refonte)
* Ordre des constructions/recherches configurable
* Chatbot d'alliance

---

**Attention**: Gardez à l'esprit que cette application est en complet désaccord avec le règlement du jeu et qu'un bannissement de vos comptes est une issue possible !

---

# Installation

### Ubuntu / Debian / Windows 10 (Linux EXT)

Soon..

### Environnement Virtuel

Tout d'abord, il faut installer `venv`, pour ce faire on utilise `pip` insatallé précédemment :

```sh
pip install venv
```

Maintenant, nous pouvons initialiser notre environnement virtuel en utilisant `Python 2.x` :

```sh
virtualenv -p /usr/bin/python2.7 cache/env
cd cache/env && source bin/activate && cd ../../
```

Puis on installe les plugins nécéssaires au fonctionnement du bot :

```sh
pip install -r cache/requirements.txt
```

# Configuration

Soon...

# Execution

Pour executer BlackLion, il vous suffit d'activer l'environnement virtuel dans votre session de terminal (si ce n'est pas déjà fait) :

```sh
cd cache/env && source bin/activate && cd ../../
```

Enfin, nous pouvons le lancer :

```sh
python ./blacklion
```

`Ctrl+C` pour arrêter le bot et déconnecter tous les comptes.

# Ressources (DEV)

* [HTTP Requests](http://requests-fr.readthedocs.io/en/latest/index.html)
* [Regex](https://docs.python.org/2/library/re.html)
* [XPath](https://docs.python.org/2/library/xml.etree.elementtree.html#xpath-support)
