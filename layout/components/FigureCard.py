import dash_bootstrap_components as dbc
from dash import html, dcc

def FigureCard(title, id, description=None):
    return dbc.Card([
        dbc.CardHeader(html.H5(title)),
        dbc.CardBody([
            dcc.Graph(id={"type": "graph", "index": id}, className="figure-card"),
            html.P(description, className="text-muted small mt-2") if description else None
        ])
    ], className="mb-4 shadow-sm")
