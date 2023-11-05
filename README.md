# IFT-4001-TP2
Application intégrant plusieurs solveurs dans le but de résoudre une variation du problème du sac à dos

## Démarrer l'application
Pour démarrer l'application vous disposez de deux options

1. lancer l'application à l'aide de Docker
2. lancer l'application localement

### lancer l'application à l'aide de Docker
Pour lancer l'application via docker il vous suffit d'installer docker sur votre machine puis de lancer le script suivant:
`docker-compose up`

Pour reconstruire l'application suite à une modification du Dockerfile ou de la configuration de l'environnement virtuel: `docker-compose up --build`

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
python3 -m __main__.py
```




