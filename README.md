# Liens

- [Drive](https://drive.google.com/drive/folders/1TO7dAfNoaHIbem9_W7PnAWPbzjFeuyRb?usp=sharing)
- [Trello](https://trello.com/b/fQlOlufG/architecture-logicielle)

# Commandes

Installer les dépendances

```bash
pip install -r requirements.txt
```

Lancer le serveur

```bash
flask -A app/main run
```

# Troubleshoot

## Import en gris

Si un import comme celui de l'exemple :

```py
from service import example;
```

> ℹ️ Import dans `main.py` d'un service dans `app/service/`

Est surligné en gris avec l'avertissement `Import "service" could not be resolved` :

Mettez ceci dans `.vscode/settings.json` :

```json
{
    "python.analysis.extraPaths": ["./app"]
}
```
