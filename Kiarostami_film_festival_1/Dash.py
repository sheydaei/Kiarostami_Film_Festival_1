import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import streamlit as st
import gdown

st.set_page_config(page_title="Kiarostami Film Festival Dashboard", layout="wide")

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
        dcc.Graph(id='gender-pie-chart', figure=px.pie(df, names='Gender', title='Gender Breakdown', hole=0.4, template="plotly_dark"))
    ]),

    html.Div([
        html.H2("Age Distribution", style={'color': 'white'}),
        dcc.Graph(id='age-histogram', figure=px.histogram(df, x="Age", title="Age Distribution", template="plotly_dark"))
    ])
], style={'backgroundColor': 'black', 'color': 'white'})

dash_app_html = app.index()

st.components.v1.html(dash_app_html, height=1000)
