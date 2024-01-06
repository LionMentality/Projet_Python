# Projet_Python

# User Guide

## 1. Prérequis
Assurez-vous que votre environnement de développement possède les éléments suivants :

- Python installé sur votre machine.
- Un gestionnaire de paquets Python tel que pip.

## 2. Installation des dépendances
1. Clonez le référentiel depuis GitHub :
    ```bash
    git clone https://github.com/LionMentality/Projet_Python.git
    ```

2. Accédez au répertoire du projet :
    ```bash
    cd votre-projet
    ```

3. Installez les dépendances nécessaires :
    ```bash
    pip install -r requirements.txt
    ```

## 3. Exécution de l'application
1. Exécutez le script principal `main.py` :
    ```bash
    python main.py
    ```

2. Ouvrez votre navigateur et accédez à l'URL suivante : [http://127.0.0.1:8050/](http://127.0.0.1:8050/).

## 4. Utilisation du Dashboard
### Histogramme du loyer moyen et des logements mis en location par année :
1. Utilisez la liste déroulante pour sélectionner l'année souhaitée.
2. Explorez l'histogramme généré pour le loyer moyen et le nombre de logements mis en location.

### Graphique de l'évolution du nombre d'habitants par région :
1. Utilisez la liste déroulante pour sélectionner la région souhaitée.
2. Explorez le graphique représentant l'évolution du nombre d'habitants au fil des années.

### Visualisation géographique : Logements sociaux et indicateurs socio-économiques :
1. Utilisez les listes déroulantes pour sélectionner l'année et le filtre souhaités.
2. Explorez la carte générée qui affiche les données géographiques.

## 5. Arrêt de l'application
Pour arrêter l'application, revenez à votre terminal où l'application est en cours d'exécution et appuyez sur `Ctrl+C`.


# Rapport d'Analyse

## Introduction

Ce rapport présente une analyse approfondie des données du projet "Logements et Indicateurs Socio-Économiques depuis 2018". L'objectif de cette analyse est de fournir des insights significatifs à partir des données disponibles et de guider les décisions futures.

## Exploration des Données

### Description Générale

Le jeu de données comprend des informations sur les logements, les indicateurs socio-économiques, et d'autres métriques pertinentes depuis 2018. Il est basé sur des sources publiques et est structuré en plusieurs colonnes.

### Statistiques Principales

- Nombre total de logements.
- Évolution du nombre d'habitants par région au fil des années.
- Taux de logements sociaux et taux de pauvreté.

## Analyse des Tendances Temporelles

### Évolution du Nombre d'Habitants

L'analyse des tendances temporelles montre une croissance constante du nombre d'habitants dans certaines régions, tandis que d'autres connaissent des variations plus marquées.

### Parc sociaux

## Analyse Géographique

### Cartographie des Indicateurs Socio-Économiques

L'analyse géographique se concentre sur la visualisation des indicateurs socio-économiques à travers une carte interactive. Elle permet d'identifier les régions présentant des caractéristiques spécifiques.

## Conclusion

L'analyse des données met en évidence plusieurs tendances et schémas significatifs. Les principales conclusions comprennent :

- Une croissance constante du nombre d'habitants dans certaines régions.
- Des variations significatives dans les taux de logements sociaux.
- Des disparités socio-économiques régionales.

# Developer Guide

Ce guide a pour objectif de fournir une compréhension approfondie de l'architecture du code.

## Structure du Projet

- **main.py:** Le script principal qui lance l'application Dash. Il importe les différents composants de l'application, tels que la mise en page (`app_layout`) et les rappels (`callbacks`).

- **app_layout.py:** Contient le code décrivant la mise en page de l'application Dash. Les éléments de l'interface utilisateur, tels que les graphiques et les listes déroulantes, sont définis ici.

- **callbacks.py:** Contient les fonctions de rappel pour les interactions entre les composants de l'interface utilisateur. Ces fonctions sont déclenchées lorsqu'un utilisateur interagit avec l'application.

- **imports.py:** Un module qui regroupe les importations nécessaires à l'ensemble du projet.

- **data.py:** Peut contenir des fonctions ou des classes liées à la gestion des données, telles que la lecture des données depuis une source externe.