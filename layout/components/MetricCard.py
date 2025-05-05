import dash_bootstrap_components as dbc
from dash import html

def MetricCard(title, id):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, className="card-title text-muted"),
            html.H4(id={"type": "metric-value", "index": id}, className="card-text")
        ]),
        className="text-center shadow-sm"
    )
