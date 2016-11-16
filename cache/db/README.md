# Configuration

Ici se trouvent tous les fichiers de configuraiton du bot. Ils sont tous au format [JSON](https://fr.wikipedia.org/wiki/JavaScript_Object_Notation) et certains n'ont normalement pas à être édité manuellement.

### Accounts

Le fichier `accounts.json` contient la liste de tous vos comptes 3GM. Un compte est représenté par la structure suivante :

```
{
    "email": "email@example.com",
    "nickname": "username",
    "password": "password",
    "server": 3,
    "group": 0
}
```

On remarques les points suivants :

* `email` : C'est l'email avec laquelle vous avez inscrit votre compte
* `nickname` : C'est votre pseudo en jeux, mais également votre nom de compte
* `password` : Le mot de passe de votre compte
* `server` : C'est le numéro de serveur (`SERVER_ID`). [1=Terra/2=Andherra/3=Dundha/etc..]
* `group` : Et enfin, le groupe de travail de votre compte. Il peut être unique ou partagé.

Si l'on souhaite ajouté un second compte dans le fichier `accounts.json`, on ajoutera tout simplement une seconde fois toutes les informations.

Exemple de fichier `accounts.json` :

```
{
    "users": [
        {
            "email": "user1@openseedbox.net",
            "nickname": "user1",
            "password": "pass1",
            "server": 3,
            "group": 0
        },
        {
            "email": "user2@openseedbox.net",
            "nickname": "user2",
            "password": "pass2",
            "server": 2,
            "group": 3
        },
        {
            "email": "user3@openseedbox.net",
            "nickname": "user3",
            "password": "pass3",
            "server": 3,
            "group": 0
        }
    ]
}
```

### Groups

Le fichier `groups.json` quand à lui, permet de dire au bot ce qu'il doit faire et quel chemin il doit suivre pour développer vos bases sur le jeu.

Soon...
