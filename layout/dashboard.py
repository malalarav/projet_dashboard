import json
import dash_bootstrap_components as dbc
from dash import html
from layout.components.MetricCard import MetricCard
from layout.components.FigureCard import FigureCard

# Charger les descriptions
with open("assets/figure_descriptions.json", encoding="utf-8") as f:
    figure_descriptions = json.load(f)

dashboard = dbc.Container([
    # METRIC CARDS (max 4)
    dbc.Row([
        dbc.Col(MetricCard("Nombre de patients", id="patients"), md=3),
        dbc.Col(MetricCard("Durée moyenne (s)", id="avg-duration"), md=3),
        dbc.Col(MetricCard("Satisfaction moyenne", id="avg-rating"), md=3),
        dbc.Col(MetricCard("% avec interruptions", id="interruption-rate"), md=3),
    ], className="mb-4"),

    # ROW 1: Durée vs dents + texte
    dbc.Row([
        dbc.Col(FigureCard("Durée vs Nombre de dents", id="duration", description=figure_descriptions.get("duration")), md=6),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("À propos du dashboard", className="card-title"),
                    html.P(
                        "Ce tableau de bord a été conçu à partir de données réelles issues de traitements chirurgicaux dentaires robotisés. "
                        "Chaque traitement comprend deux phases : la configuration initiale (setup) et l'exécution automatisée (treatment). "
                        "Le robot peut être interrompu par le dentiste ou automatiquement, et les erreurs logicielles sont enregistrées.",
                        className="mb-2"
                    ),
                    html.P(
                        "Ce dashboard interactif met en lumière l'impact de facteurs comme le nombre de dents traitées, les interruptions ou les erreurs "
                        "sur la satisfaction du patient et du praticien. Il permet d’explorer les corrélations et tendances clés, et d’identifier les "
                        "leviers d’amélioration pour optimiser l’expérience globale du traitement.",
                        )
                        ]),
                className="figure-card"
            ), md=6
        )
    ], className="mb-4"),

    # ROW 2 : Deux satisfactions
    dbc.Row([
        dbc.Col(FigureCard("Satisfaction vs Interruptions", id="interruptions", description=figure_descriptions.get("interruptions")), md=6),
        dbc.Col(FigureCard("Satisfaction vs Erreurs", id="errors", description=figure_descriptions.get("errors")), md=6)
    ], className="mb-4"),

    # ROW 3 : Heatmap + Relation
    dbc.Row([
        dbc.Col(FigureCard("Matrice de corrélation", id="correlation", description=figure_descriptions.get("correlation")), md=6),
        dbc.Col(FigureCard("Relation sélectionnée", id="relation-detail", description=figure_descriptions.get("relation-detail")), md=6)
    ], className="mb-4")
], fluid=False, className="section")
