# gardener
script en python3 qui permet de gérer ses comptes à travers l'api [leekwars](https://leekwars.com) :
- lancement des fights automatisés selon un *behavior* et choisit les adversaires selon une *strategy*
- attend le résultat de chaque fight pour lancer la suivante (ou pas..)
- dépense le capital dans une stat spécifique
- s'incrit aux tournois
- achète un pack de 100 fights avec des habs
- permet la synchronisation des ias entre les comptes et avec du code local

![gardener](https://i.imgur.com/L6sgsHJ.png)

## usage

nécessite [python3](https://www.python.org/downloads/) et [pip](https://pypi.org/project/pip/)

- git clone https://github.com/tagadanar/leekwars_gardener.git
- configurer ses comptes dans le fichier settings.py
- pip install -r requirements.txt
- python main.py

### settings.py

chaque compte utilisateur est représenté par un dictionnaire {} python possédant les attributs suivants :

- login (required)
- password (required)
- behavior (required)
- strategy (facultative)
- buy_fight (facultative)
- limit (required si behavior != TODOLIST || behavior != NONE)
- team_limit (facultative)
- todolist (required si behavior == TODOLIST)
- tournaments (facultative)
- goals (facultative)
- synchronize (facultative)

**behavior** correspond à un comportement à adopter dans le potager une fois connecté, actuellement les comportements disponibles sont :

- _NONE_ : ne fait rien de plus que se connecter au compte (refresh la dernière connexion, permet la synchronisation et l'inscription aux tournois)  
- _TODOLIST_ : execute la todolist, sans se soucier de la **limit** pour le stock de fight  
- _FARMING_ : ne fait que des fights éleveurs jusqu'à atteindre **limit**  
- _EQUALIZE_ : regroupe le niveau des leeks puis fait des fights farmer jusqu'à atteindre **limit**  
- _BALANCED_ : tente de répartir les fights disponibles entre chaque leek et l'éleveur jusqu'à atteindre **limit**  
- _SOLO\_BALANCED_ : tente de répartir les fights disponibles entre chaque leek jusqu'à atteindre **limit**  
- _SOLO\_X_ : ne fait que des fights solo avec le leek *X* (X étant une valeur entre 1 et 4 correspondant au leek désiré) jusqu'à atteindre **limit**   

**strategy** correspond à la stratégie à adopter pour choisir l'adversaire dans le potager, actuellement les comportements disponibles sont :

- _RANDOM_ : choisi un adversaire aléatoire (par défaut si aucune stratégie n'est défini pour le compte)
- _BEST_ : choisi l'adversaire au talent le plus élevé
- _WORST_ : choisi l'adversaire au talent le plus bas

**buy_fight** correspond à un boolean, si il est *True*, le script tentera d'acheter un pack de combat avec des habs **avant le run**  
les fights seront donc utilisées immédiatement après par le script, à moins que la **limit** ou la todolist l'en empêche.

**team_limit** si il n'est pas renseigné, ne fera pas de team fight.  
Si il est renseigné, ce doit être un entier positif (0 à n) indiquant le nombre de fight à garder (de la même manière que fonctionne **limit**)  
Le script tentera de lancer des fights de team avec toutes les compos où vos leeks sont présents, jusqu'à atteindre **team_limit**

**todolist** correspond à un dictionnaire {}, avec pour clé les constantes de la class g (cf. utils.py), où FARMER représente les combats d'éleveurs, et LEEK\_1/2/3/4 représentent les 4 leeks d'un compte, dans l'ordre de leur création (et donc dans leur ordre sur le site)  
les valeurs sont le nombre de combats à réaliser avec chaque clé.

**tournaments** correspond à une liste [], avec pour valeur les constantes de la class g (cf. utils.py), où FARMER représente le compte et LEEK\_1/2/3/4 représentent les 4 leeks d'un compte, dans l'ordre de leur création (et donc dans leur ordre sur le site)  
le script tentera d'inscrire aux tournois chaque valeur dans la liste.

**goals** correspond à un dictionnaire {}, avec pour clé les constantes de la class g, uniquement LEEK\_1/2/3/4, auquel on peut associer un comportement pour la dépense de point de capital (cf. la class goals dans utils.py)

**synchronize** correspond à un dictionnaire {} avec jusqu'à 4 sous params:  
- **directory** (required) qui indique le path (relatif à l'emplacement du main.py ou absolu) du dossier contenant l'ia
- **transfer** (required) qui indique le sens de la synchronisation, montante (g.UPLOAD) ou descendante (g.DOWNLOAD)
- **version** (facultatif) précise la version du script créé au moment de l'upload si le fichier n'existe pas, '1.1' par défaut si non précisé, les seuls valeurs valides à ma connaissance sont 1.0 et 1.1 actuellement
- **ignore** (facultatif) un tableau de string indiquant les fichiers que vous ne voulez pas upload sur leekwars, pour le moment pas de regex, juste une comparaison de string simple, mais ça permet déjà d'ignorer le .git ^^

### configurations générales

**fight** (facultative)

paramètre permettant d'utiliser les combats dans le potager, peut prendre 3 valeurs :  
state.OFF **(valeur par défaut)** : n'ira pas se battre dans le potager  
state.ASK : demande au lancement si le script doit combattre dans le potager  
state.ON : se battera dans le potager selon le **behavior** du compte

**speedrun** (facultative)

paramètre permettant d'ignorer l'attente entre les fights (à utiliser avec parcimonie), peut prendre 3 valeurs :  
state.OFF **(valeur par défaut)** : attendra entre chaque fight, comportement normal  
state.ASK : demande au lancement si le script doit faire un speedrun  
state.ON : n'attendra pas le résultat de la fight pour lancer la suivante

```
/!\ attention lors d'un speedrun l'attribution du capital ne peut plus fonctionner. /!\
```

**shutdown** (facultative)

paramètre permettant d'éteindre le pc à la fin du script, peut prendre 3 valeurs :  
state.OFF **(valeur par défaut)** : n'éteindra pas le pc  
state.ASK : demande au lancement si le script doit éteindre le pc  
state.ON : éteindra le pc à la fin du script

**synchronize** (facultative)

paramètre permettant la synchronisation des ias, peut prendre 3 valeurs :  
state.OFF **(valeur par défaut)** : ne synchronisera pas vos ias  
state.ASK : demande au lancement si le script doit synchroniser les ias  
state.ON : synchronisera systématiquement les ias

```
/!\ attention, une mauvaise configuration vous expose à la perte de votre code /!\  
```

par précaution gardez toujours une copie de votre code de côté avant de jouer avec cette option !  
dans le doute, laissez l'option sur **OFF**.

la synchronisation des ias se fera dans l'ordre de déclaration des comptes, une configuration enviable est donc d'avoir en premier compte votre compte actif où vous codez régulièrement sur le site, avec une config :

```js
'synchronize': {
    'directory': './path_to_ia_dir',
    'transfer': g.DOWNLOAD,
}
```
qui permettra de ramener en local les changements que vous avez fait sur le site.  
puis sur tous vos comptes suivant une config :

```js
'synchronize': {
    'directory': './path_to_ia_dir',
    'transfer': g.UPLOAD,
}
```
qui mettra à jour les ias de vos autres comptes sur le site depuis l'ia récupéré sur le premier compte.

Une autre configuration pourrait être d'avoir tous vos comptes en UPLOAD, pour pouvoir coder en local et rapidement répercuter les changements sur tous vos comptes.

NB. la synchronisation ne fait pas de purge, elle se contente d'écraser les fichiers déjà existant avec le nouveau contenu, et créer les fichiers/dossiers inexistant.  
NB² pour le moment toutes les ias sont upload en lsv1, quand le lsv2 arrivera je mettrais ce script à jour, et un nouveau param sera disponible pour préciser la version du langage.

### command line option

certaines commandes peuvent être ajouté à l'appel pour ignorer la valeur d'un param dans setting.py:

**-f --fight** fait les combats même si **fight** est config sur OFF  
**-nf --no-fight** ne fait pas les combats même si **fight** est config sur ON  
**-sr --speedrun** fait un speedrun même si **speedrun** est config sur OFF  
**-nsr --no-speedrun** ne fait pas un speedrun même si **speedrun** est config sur ON  
**-s --sync** fait la synchronisation de l'ia même si **synchronize** est sur OFF  
**-ns --no-sync** ne fait pas la synchronisation de l'ia même si **synchronize** est sur ON
