import dash
from dash import html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import webbrowser
from threading import Timer

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("CSV Data Viewer", className="text-center my-4"))),
    
    dbc.Row(dbc.Col([
        dbc.InputGroup([
            dbc.Input(
                id="csv-url",
                value="https://raw.githubusercontent.com/plotly/datasets/master/iris.csv",
                placeholder="Enter CSV URL"
            ),
            dbc.Button("Load", id="load-button", color="primary")
        ], className="mb-3")
    ], width={"size": 10, "offset": 1})),
    
    dbc.Row(dbc.Col(html.Div(id="table-container"), width=12))
], fluid=True)

@app.callback(
    Output("table-container", "children"),
    [Input("load-button", "n_clicks")],
    [State("csv-url", "value")]
)
def update_table(n_clicks, url):
    if n_clicks is None:
        df = pd.read_csv(url, sep=None, engine='python')
        return create_table(df)
    
    df = pd.read_csv(url, sep=None, engine='python')
    return create_table(df)

def create_table(df):
    return [
        html.H5(f"{df.shape[0]} rows × {df.shape[1]} columns", className="text-muted mb-3"),
        dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_table={"height": "600px", "overflowY": "auto", "overflowX": "auto"},
            style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
            style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}]
        )
    ]

if __name__ == "__main__":
    server = app.server