# gardener
script en python3 qui permet de gérer ses comptes à travers l'api leekwars  
le script attend le résultat de chaque fight pour lancer la suivante

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
- limit (required si behavior != TODOLIST || behavior != NONE)
- todolist (required si behavior == TODOLIST)
- tournaments (facultative)
- goals (facultative)

**behavior** correspond à un comportement à adopter une fois connecté, actuellement les comportements disponibles sont :

_NONE_ : ne fait rien de plus que se connecter au compte  
_TODOLIST_ : execute la todolist, sans se soucier de la **limit** pour le stock de fight  
_FARMING_ : ne fait que des fights éleveurs jusqu'à atteindre **limit**  
_EQUALIZE_ : regroupe le niveau des leeks puis fait des fights farmer jusqu'à atteindre **limit**  
_BALANCED_ : tente de répartir les fights disponibles entre chaque leek et l'éleveur jusqu'à atteindre **limit**  
_SOLO\_BALANCED_ : tente de répartir les fights disponibles entre chaque leek jusqu'à atteindre **limit**  
_SOLO\_X_ : ne fait que des fights solo avec le leek *X* (X étant une valeur entre 1 et 4 correspondant au leek désiré) jusqu'à atteindre **limit**   


**todolist** correspond à un dictionnaire {}, avec pour clé les constantes de la class g (cf. utils.py), où FARMER représente les combats d'éleveurs, et LEEK\_1/2/3/4 représentent les 4 leeks d'un compte, dans l'ordre de leur création (et donc dans leur ordre sur le site)  
les valeurs sont le nombre de combats à réaliser avec chaque clé.

**tournaments** correspond à une liste [], avec pour valeur les constantes de la class g (cf. utils.py), où FARMER représente le compte et LEEK\_1/2/3/4 représentent les 4 leeks d'un compte, dans l'ordre de leur création (et donc dans leur ordre sur le site)  
le script tentera d'inscrire aux tournois chaque valeur dans la liste.

**goals** correspond à un dictionnaire {}, avec pour clé les constantes de la class g, uniquement LEEK\_1/2/3/4, auquel on peut associer un comportement pour la dépense de point de capital (cf. la class goals dans utils.py)

**shutdown** (required)

paramètre permettant d'éteindre le pc à la fin du script, peut prendre 3 valeurs :  
shutdown.OFF : n'éteindra pas le pc  
shutdown.ASK : demande au lancement si le script doit éteindre le pc  
shutdown.ON : éteindra le pc à la fin du script
