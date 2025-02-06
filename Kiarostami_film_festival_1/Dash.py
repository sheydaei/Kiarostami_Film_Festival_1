
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import streamlit as st
import os
import gdown



st.title("🎬 Kiarostami Short Film Festival Dashboard")

FILE_ID = "1HDY03kLu4vdjbwnLc261gxKWl__ef_nV"
url = f"https://drive.google.com/uc?id={FILE_ID}"

csv_path = "Final_Final2.csv"
gdown.download(url, csv_path, quiet=False)

df = pd.read_csv(csv_path)

df = df.drop(['Unnamed: 0'], axis=1)

df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
df['Gender'] = df['Gender'].replace({
    'male': 'Male',           
    'female': 'Female',       
    'unknown': 'Other'
})

df3 = df[(df["Production Year"] > 1995) & (df["Production Year"] < 2025)]
df3['Inspired_By_Kiarostami_clean'] = df3['Inspired_By_Kiarostami_clean'].replace({
    'Other ways': 'Loosely Inspired'
})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Kiarostami Short Film Festival", style={'textAlign': 'center', 'color': 'white'}),  

    html.Div([
        html.H3("Total Participants", style={'color': 'white'}),
        html.H1(f"{df3.shape[0]}", style={'color': 'white'})
    ], style={'backgroundColor': 'black', 'padding': '20px', 'borderRadius': '10px', 'width': '30%', 'margin': '10px'}),

    html.Div([
        html.H3("Total Movies", style={'color': 'white'}),
        html.H1(f"{df.shape[0]}", style={'color': 'white'})
    ], style={'backgroundColor': 'black', 'padding': '20px', 'borderRadius': '10px', 'width': '30%', 'margin': '10px'}),

    html.Div([
        html.H2("Gender Breakdown", style={'color': 'white'}),
        dcc.Graph(id='gender-pie-chart')
    ]),

    html.Div([
        html.H2("Age Distribution", style={'color': 'white'}),
        dcc.Graph(id='age-histogram')
    ]),

    html.Div([
        html.H2("Countries Represented", style={'color': 'white'}),
        html.Div(id='country-table')
    ]),

    html.Div([
        html.H2("Films Inspired by Kiarostami", style={'color': 'white'}),
        dcc.Graph(id="bar-chart"),
        dcc.RangeSlider(
            id='year-slider',
            min=int(df3["Production Year"].min()),
            max=int(df3["Production Year"].max()),
            value=[int(df3["Production Year"].min()), int(df3["Production Year"].max())],
            marks={int(year): str(year) for year in sorted(df3["Production Year"].unique())},
            step=1
        )
    ])
], style={'backgroundColor': 'black', 'color': 'white'})

@app.callback(
    Output('age-histogram', 'figure'),
    Input('age-histogram', 'id')
)
def update_histogram(_):
    fig = px.histogram(df, x="Age", title="Age Distribution", template="plotly_dark")
    return fig

@app.callback(
    Output('gender-pie-chart', 'figure'),
    Input('gender-pie-chart', 'id')
)
def update_pie_chart(_):
    fig = px.pie(df, names='Gender', title='Gender Breakdown', hole=0.4, template="plotly_dark")
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
