# Analyse du Paludisme en Afrique

Application d'analyse prédictive du paludisme utilisant Python (Flask) et React.

## Structure du Projet

```
malaria/
├── api/                # Backend Flask
│   ├── app.py         # Point d'entrée Flask
│   └── malaria_analysis_french.py  # Logique d'analyse
├── frontend/          # Frontend React
├── data/             # Données d'exemple
└── static/           # Fichiers statiques
```

## Technologies Utilisées

- **Backend**: Flask (Python 3.12)
- **Frontend**: React avec Material-UI
- **Analyse de Données**: pandas, scikit-learn
- **Visualisation**: matplotlib, seaborn

## Configuration Requise

- Python 3.12
- Node.js 18+
- npm ou yarn

## Installation

### Backend

```bash
# Installer les dépendances Python
pip install -r requirements.txt

# Lancer le serveur Flask
python -m flask --app api/app run
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## Déploiement

### Backend (Vercel)

Le backend est automatiquement déployé sur Vercel lors du push sur la branche principale.

### Frontend (Vercel)

1. Mettre à jour .env.production avec l'URL de l'API
2. Déployer le frontend sur Vercel

## Variables d'Environnement

### Production
- `REACT_APP_API_URL`: URL de l'API en production

### Développement
- `REACT_APP_API_URL`: http://localhost:5000/api

## Tests

```bash
python test_api.py
```

## Licence

MIT
