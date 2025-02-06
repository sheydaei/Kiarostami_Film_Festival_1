import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import streamlit as st

# 📌 تنظیمات صفحه در Streamlit
st.set_page_config(page_title="Kiarostami Film Festival Dashboard", layout="wide")

st.title("🎬 Kiarostami Short Film Festival Dashboard")

# 📌 خواندن فایل CSV از GitHub (لینک `raw.githubusercontent.com` رو چک کن)
csv_url = "https://raw.githubusercontent.com/sheydaei/My-projects/main/Kiarostami_film_festival_1/Final_Final2.csv"
df = pd.read_csv(csv_url)

# 📌 پردازش داده‌ها
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

# 📌 ساخت داشبورد Dash
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

# 📌 اجرای Dash در Streamlit
from flask import Flask
flask_app = Flask(__name__)
dash_app = dash.Dash(__name__, server=flask_app, requests_pathname_prefix="/dash/")
dash_app.layout = app.layout

st.write("🔹 **Loading Dashboard...**")
st.components.v1.iframe("https://your-streamlit-app-url/dash/", height=800)
