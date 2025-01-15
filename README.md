# API HackR

Bienvenue sur la documentation de l'API HackR ! Le README fournit toutes les informations nécessaires pour comprendre à quoi sert l'API, comment l'utiliser, et comment l'installer.

## Objectif de l'API

Cette API est une application Flask développée en Python. Elle permet de faire des choses répréhensibles à la loi, donc c'est plus mon problème après.

## Fonctionnalités et Endpoints

Voici la liste des endpoints disponibles, ce qu'ils permettent de faire, et les autorisations nécessaires pour les exécuter :

### 1. GET /easterEgg

Description : Surprise.

Autorisations nécessaires : Aucunes, même les cons sont invités.

### 2. POST /vulnerablePassword

Description : Vérifi si le mot de passe fait partie d'une liste de mots de passe les plus utilisées.

Autorisations nécessaires : Authentifié.

### 3. POST /securePasswordGeneration

Description : Génère un mot de passe sécurisé.

Autorisations nécessaires : Authentifié.

### 4. GET /fakeIdentity

Description : Génère une fausse identité.

Autorisations nécessaires : Authentifié.

### 5. POST /users

Description : Créer un utilisateur.

Autorisations nécessaires : Authentifié (admin).

### 6. GET /users

Description : Affiche la liste des utilisateurs.

Autorisations nécessaires : Authentifié (admin).

### 7. GET /logs

Description : Affiche les logs.

Autorisations nécessaires : Authentifié (admin).

### 8. POST /authentication

Description : Permet de s'authentifier.

Autorisations nécessaires : Aucunes.

### 9. POST /ddos

Description : À utiliser avec parcimonie.

Autorisations nécessaires : Authentifié (admin).

### 10. GET /randomFace

Description : Génère un visage aléatoire.

Autorisations nécessaires : Authentifié.

### 11. POST /crawler

Description : Récupère les informations d'un utilisateur.

Autorisations nécessaires : Authentifié.

### 12. POST /isValidEmail

Description : Vérifi la validité d'une adresse mail.

Autorisations nécessaires : Authentifié.

## Procédure d'installation

Voici les étapes nécessaires pour installer et exécuter le projet en local :

### Prérequis

Python 3.10 installé sur votre machine.

Un environnement virtuel pour isoler les dépendances.

### Étapes

Clonez le dépôt : 
- git clone https://github.com/justRB/api-rest.git

Créez et activez un environnement virtuel :

- python3.10 -m venv env
- source env/bin/activate  # Sur Windows : env\Scripts\activate

Installez les dépendances :

- pip install -r requirements.txt

Lancez l’application Flask :

- flask --app main run --debug

Accédez à l’API dans votre navigateur ou avec un client comme Postman :

URL par défaut : http://127.0.0.1:5000

### Structure du projet

Voici un aperçu de la structure du projet :

├── main.py                # Fichier principal contenant l'application Flask. \
├── requirements.txt       # Liste des dépendances. \
├── db.sqlite              # Base de données. \
├── decorators/            # Décorateurs. \
├── config/                # Fichiers de configuration. \
├── services/              # Logique métier. \
├── apis/                  # Contrôleurs API. \
├── documents/             # Documents. \
└── README.md              # Documentation du projet.
