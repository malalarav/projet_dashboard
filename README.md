# 🦷 Dashboard d'analyse des traitements dentaires automatisés

Ce projet propose un dashboard interactif développé en Python avec [Dash](https://dash.plotly.com/), permettant d'explorer des données issues de traitements chirurgicaux robotisés dans le domaine dentaire.

---

## 🎯 Objectif

À partir d’un fichier CSV contenant les informations sur les traitements (durée, interruptions, erreurs, satisfaction patient/praticien, etc.), ce dashboard permet :

- D’analyser l’impact de divers facteurs (durée, nombre de dents, erreurs, interruptions) sur la satisfaction
- D’explorer visuellement les corrélations entre les variables
- D’offrir un outil interactif au praticien ou à l’analyste pour mieux comprendre les résultats et l’expérience patient

---

## 🛠️ Technologies utilisées

- Python 3.x
- [Dash](https://dash.plotly.com/) (Plotly)
- Dash Bootstrap Components
- Pandas
- Plotly Express

---

## 📁 Fichiers principaux

| Fichier/Dossier            | Rôle |
|----------------------------|------|
| `app.py`                   | Script principal qui lance le dashboard |
| `DataScienceTreatmentData.csv` | Données brutes du projet |
| `layout/`                  | Structure du layout Dash |
| `layout/components/`       | Composants réutilisables (`MetricCard`, `FigureCard`) |
| `assets/`                  | CSS et texte explicatif (`style.css`, `figure_descriptions.json`) |
| `README.md`                | Ce fichier de documentation |

---

## 🚀 Lancer l'application en local

### 1. Cloner le repo
```bash
git clone https://github.com/malalarav/projet_dashboard.git
cd projet_dashboard
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer l'app

---

## 🙏 Remerciements & inspiration

Ce projet s'inspire fortement du style et de l'organisation du dashboard [Streaming Metrics](https://github.com/cmd-ntrf/streaming-metrics), que j'ai adapté à un autre jeu de données et à un contexte clinique.

Merci à son auteur pour la qualité du code et du design.

