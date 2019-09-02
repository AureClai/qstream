QStream - Plugin QGIS pour Stream
======

Qu'est ce que QStream
------
### Contexte
"Stream - simulateur du trafic événementiel", est un outil de simulation dynamique développé sous Python par le Cerema. Stream prend en entrée des données de diverses natures. En particulier, le coeur de la donnée est la description du réseau sous forme de graphe où la topologie des liens est fondamentale.
Le logiciel QGIS est le logiciel open source de référence pour gérer des formats de données variés, intégrant leur dimension géographique. QGIS permet d'intégrer des plugins personnalisés avec le package Qt de Python. Ces plugins contiennent les éléments de base de toute interface graphique : des widgets, boutons, du texte et des images.

### Intérêt
QStream est le plugin QGIS dédié pour la définition manuelle des scénarios pour en réaliser une simulation dynamique à l'aide de l'outil Stream. Plus généralement, QStream est l'interface homme machine (IHM) de Stream.

### Principe général et fonctionnement
QStream est une interface graphique, permettant de manipuler le logiciel Stream, définir ses entrées et traiter ses sorties.
En particulier, pour la définition des entrées, QStream permet d'éditer le réseau routier d'intérêt, de définir la demande de déplacement sur ce réseau, de définir des régulations, le tout sous la forme d'un geopackage. Il ne nécessite pas d'avoir été relié au logiciel Stream pour réaliser ces tâches.
Pour les trois tâches suivantes, QStream appelle des fonctions de Stream permettant de réaliser les différentes actions :
- manipulation de Stream : QStream transforme les données d'entrées en un fichier .npy (format de sauvegarde du module Python numpy), lance le logiciel Stream lorsque celui-ci a été détecté par QStream, et retourne un fichier de sortie contenant les sorties brutes de la simulation sous un format .npy ;
- analyse des sorties : QStream charge le .npy des sorties de simulation, et permet d'effectuer divers traitements pour reconstituer des indicateurs ponctuels (débits, vitesses, concentrations) ou sur des itinéraires (temps de parcours), et ressort des graphiques pour analyser ces variables.
- export des sorties : QStream charge les sorties de simulation et produit des tableaux sous format .csv contenant les débits et temps de parcours.

### Implémentation
QStream est développé en tant qu'extension du logiciel QGIS 3. De ce fait, il est écrit en langage Python et fait appel à la librairie Qt5. Les différents modules ont été designés grâce au logiciel open source Qt designer. Pour information, l'ensemble des logiciels utilisé est inclus dans le téléchargement du logiciel QGIS.

Où l'obtenir
---
A venir (Github Cerema)

Installation
---
### Installation de ```pyexcel_ods```
1. Ouvrir l'invite de commande OSGEO4W en administrateur
2. Taper ```py3_env```
3. Taper ```qt5_env```
4. Taper ```pip install pyexcel_ods```
   
### Installation du plugin

5. Compresser le dossier *qstream* dans une archive ZIP (.zip).
6. Dans Qgis :
   1. Extension
   2. Installer / Gérer les extensions
   3. Installer depuis un ZIP
   4. Rechercher l'archive crée en étape 1
7. Charger QStream dans le gestionnaire de plugin
8. Cliquer sur l'icône invisible dans la barre des outils QGIS.
9.  Avec QStream, importer le fichier d'exemple `data.gpkg` pour tester l'installation.

Utilisation
---
Le guide d'utilisation est disponible dans :
```
qstream/doc/index.html
```
Il est aussi possible de l'ouvrir directement depuis le plugin QStream grâce au *"?"* en haut à droite de l'IHM.

Contact
---
aurelien.clairais@cerema.fr

Bugs
---
Voir contact.

Licence
---
QStream est sous licence [GPL](https://www.gnu.org/licenses/gpl-3.0.txt)




