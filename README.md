# Installation
Ce projet utilise **uv** pour gérer les dépendances et l'environnement virtuel.

1. Pour installer **uv**, utilisez le lien suivant : [Installation de uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Une fois installé, lancez la commande `uv sync` pour télécharger les dépendances et initialiser l'environnement.

# Utilisation
Pour utiliser l'assistant, lancez la commande suivante :  
`uv run src/app.py`

# Variables d'environnement
Pour configurer l'accès à OpenAI, il faut placer à la racine du projet un fichier `.env` comme suit :

```
OPENAI_API_KEY=XXXX
```