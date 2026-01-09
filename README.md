# Real-Estate-Stats-API (Demo Project)

![CI](https://github.com/Sewake/Real-Estate-Stats-API/actions/workflows/ci.yml/badge.svg)

## 🚀 Setup Instructions

## Pré-requis

- Docker & Docker Compose
- GNU Make
- Python 3.12 (optionnel, si exécuté en dehors de Docker)


## Stack technique

- Python 3.12
- Django 6
- Django REST Framework
- PostgreSQL 16
- Docker & Docker Compose
- pytest


## 🔨 1. Build & Démarrer la Stack
Avant de démarrer, créer un fichier .env. Vous pouvez utiliser le fichier .env.example comme référence:

```
cp .env.example .env
```

Puis démarrer l'environnement docker:
```
make build
```

Cela va démarrer les services:
- web: l'app Django avec autoreload
- db: La BDD PostgreSQL 16 


Formulaire utilisateur: http://localhost:8000/
Admin: http://localhost:8000/admin/



## 🗃️ 2. Lancer les migrations de base de données
```
make migrate
```


## 📦  3. Importer le dataset

Glisser les fichiers .CSV dans `app/data/dataset` puis lancer


```
make loaddata
```


## 🧪 4. Éxécuter la suite de tests

```
make test
```


## 5. 🧹 Qualité de code & pre-commit

Ce projet utilise pre-commit pour garantir un code propre et cohérent avant chaque commit.

Outils exécutés automatiquement :
- flake8 (lint)
- black (formatage)
- isort (imports)
- pyupgrade

**Installation de pre-commit**

Installer l’outil (une seule fois) :

```
pip install pre-commit
```

Activer les hooks dans le repository :
```
pre-commit install
```

À partir de là, les hooks s’exécuteront automatiquement à chaque git commit.


## 6. 📦 Commandes Makefile


| Commande               | Description             |
|-----------------------|-------------------------|
| `make build`          | Build & démarre Docker  |
| `make down`           | Stop les containers     |
| `make migrate`        | Applique les migrations django     |
| `make loaddata`       | Load le dataset         |
| `make test`           | Run pytest              |
| `make lint`           | Run flake8              |
| `make format`         | Run isort + black       |
| `make pre_commit_run` | Run tout les pre-commit hooks|