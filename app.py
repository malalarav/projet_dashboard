import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from layout.dashboard import dashboard

# === Données ===
df = pd.read_csv("DataScienceTreatmentData.csv", sep=";")

# Nettoyage/typage
cols = ["PatientRating", "DoctorRating", "TreatmentDuration(sec)", "SetupDuration(sec)",
        "NumberOfTeeth", "Interruptions", "Errors"]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["TotalDuration(sec)"] = df["SetupDuration(sec)"] + df["TreatmentDuration(sec)"]
df["TreatmentPerTooth(sec)"] = df["TreatmentDuration(sec)"] / df["NumberOfTeeth"]

def get_clean_df():
    return df.dropna(subset=cols)

# === App Dash ===
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # pour déploiement

app.layout = html.Div([
    html.H1("Dashboard : Analyse des traitements dentaires automatisés", className="mb-4"),
    dashboard
], id="page")

# === Callbacks : METRICS ===
@app.callback(
    Output({"type": "metric-value", "index": "patients"}, "children"),
    Output({"type": "metric-value", "index": "avg-duration"}, "children"),
    Output({"type": "metric-value", "index": "avg-rating"}, "children"),
    #Output({"type": "metric-value", "index": "error-rate"}, "children"),
    Output({"type": "metric-value", "index": "interruption-rate"}, "children"),
    Input("page", "id")
)
def update_metrics(_):
    df_clean = get_clean_df()
    n = df_clean.shape[0]
    avg_duration = df_clean["TotalDuration(sec)"].mean()
    avg_rating = df_clean["PatientRating"].mean()
    #error_pct = (df_clean["Errors"] > 0).mean() * 100
    interruption_pct = (df_clean["Interruptions"] > 0).mean() * 100

    return (
        f"{n}",
        f"{avg_duration:.1f} s",
        f"{avg_rating:.2f} / 5",
        #f"{error_pct:.0f}%",
        f"{interruption_pct:.0f}%"
    )


# === Graph 1 : Durée vs Dents ===
@app.callback(
    Output({"type": "graph", "index": "duration"}, "figure"),
    Input("page", "id")
)
def plot_duration(_):
    df_clean = get_clean_df()
    fig = px.scatter(df_clean, x="NumberOfTeeth", y="TreatmentDuration(sec)",
                     color="PatientRating", trendline="ols",
                     labels={"NumberOfTeeth": "Nombre de dents", "TreatmentDuration(sec)": "Durée (s)"})
    return fig

# === Graph 2 : Satisfaction vs Interruptions ===
@app.callback(
    Output({"type": "graph", "index": "interruptions"}, "figure"),
    Input("page", "id")
)
def plot_interruptions(_):
    df_clean = get_clean_df()
    grouped = df_clean.groupby("Interruptions")[["PatientRating", "DoctorRating"]].mean().reset_index()
    fig = px.line(grouped, x="Interruptions", y=["PatientRating", "DoctorRating"],
                  markers=True, labels={"value": "Note", "Interruptions": "Nombre d'interruptions"})
    return fig

# === Graph 3 : Satisfaction vs Erreurs ===
@app.callback(
    Output({"type": "graph", "index": "errors"}, "figure"),
    Input("page", "id")
)
def plot_errors(_):
    df_clean = get_clean_df()
    grouped = df_clean.groupby("Errors")[["PatientRating", "DoctorRating"]].mean().reset_index()
    fig = px.line(grouped, x="Errors", y=["PatientRating", "DoctorRating"],
                  markers=True, labels={"value": "Note", "Errors": "Erreurs"})
    return fig

# === Graph 4 : Heatmap de corrélation ===
@app.callback(
    Output({"type": "graph", "index": "correlation"}, "figure"),
    Input("page", "id")
)
def plot_correlation(_):
    df_clean = get_clean_df()
    corr = df_clean[cols].corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r")
    fig.update_layout(title="Corrélations entre les variables")
    return fig

# === Graph 5 : Relation sélectionnée via heatmap ===
@app.callback(
    Output({"type": "graph", "index": "relation-detail"}, "figure"),
    Input({"type": "graph", "index": "correlation"}, "clickData")
)
def show_relation(clickData):
    df_clean = get_clean_df()

    if not clickData:
        fig = go.Figure()
        fig.update_layout(title="Cliquez sur une cellule de la heatmap pour explorer une relation")
        return fig

    var_x = clickData['points'][0]['x']
    var_y = clickData['points'][0]['y']

    if var_x == var_y or var_x not in df_clean or var_y not in df_clean:
        fig = go.Figure()
        fig.update_layout(title="Sélection non valide")
        return fig

    data = df_clean[[var_x, var_y]].dropna()
    if data.empty:
        return go.Figure().update_layout(title="Aucune donnée disponible")

    is_x_cat = data[var_x].nunique() < 10
    is_y_cat = data[var_y].nunique() < 10

    if is_x_cat and not is_y_cat:
        return px.box(data, x=var_x, y=var_y, title=f"{var_y} en fonction de {var_x}")
    elif not is_x_cat and not is_y_cat:
        return px.scatter(data, x=var_x, y=var_y, trendline="ols", title=f"{var_y} en fonction de {var_x}")
    else:
        return px.histogram(data, x=var_x, color=var_y, barmode="group", title=f"{var_y} réparti par {var_x}")

# === Run ===
if __name__ == "__main__":
    app.run(debug=True)
