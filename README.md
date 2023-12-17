# IFT-4001-TP2
Application intégrant plusieurs solveurs dans le but de résoudre une variation du problème du sac à dos

## Démarrer l'application
Pour démarrer l'application vous disposez de deux options

1. lancer l'application à l'aide de Docker
2. lancer l'application localement

### lancer l'application à l'aide de Docker
Pour lancer l'application via docker il vous suffit d'installer docker sur votre machine puis de lancer le script suivant:
`docker-compose up ift-4001-tp2`
Pour reconstruire l'application suite à une modification du Dockerfile ou de la configuration de l'environnement virtuel: `docker-compose up --build ift-4001-tp2`

#### Si vous souhaitez voir les données sauvegardées dans les tables
Vous pouvez lancer pgadmin avec la commande suivante `docker-compose up pgadmin`.
Puis rendez-vous à l'url suivant [pgadmin](http://localhost:8888/)
Vous pourrez vous connecter en utilisant l'e-mail admin@admin.com et le mot de passe root. Si c'est la première fois que vous exécutez pgadmin il se peut que cela prenne un certain temps.

Par la suite vous devrez vous connecter à la base de données. En haut à gauche de la page faites un click droit sur le mot server
puis 
* register -> server 
* Nommez le serveur, nous recommandons de l'appeler ift-4001-tp2
* allez dans l'onglet connection
* le host name est postgres
* le username est postgres
* le mot de passe est postgres123
* cliquez sur save

Et voilà! vous avez accès aux données.

### Arrêter le logiciel et toute ses dépendances
exécutez `docker-compose down`

### Effacer les conteneur de votre ordinateur
exécutez 'docker system prune --all'

### lancer l'application localement
Vous aurez de bonne chances d'être dépendant de votre système d'opération. Vous devrez sans doute regénérer le fichier ift_4001_tp2.yml

En supposant que vous avez un fichier d'environnement compatible avec votre système d'opération et que vous avez installé anaconda3 sur votre machine.
#### Vous pouvez construire le projet avec les étapes suivantes

1. `conda env create -f ift_4001_tp2.yml`
2. `conda activate ift-4001-tp2`

#### Vous pouvez par la suite lancer l'application avec la commande suivante

```shell
python3 .
```
ou
```shell
python3 -m __main__
```

## Références au problème

ci-dessous se trouve une liste de références à la modélisation ou à des pistes de solutions au problème

* https://en.wikipedia.org/wiki/Packing_problems
* https://www.minizinc.org/doc-2.7.6/en/lib-globals-packing.html
* https://stackoverflow.com/questions/7392143/python-implementations-of-packing-algorithm
* https://minizinc-python.readthedocs.io/en/latest/getting_started.html



