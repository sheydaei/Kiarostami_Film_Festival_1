import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
import streamlit as st
import flask
import threading
import time

# 📌 تنظیمات صفحه در Streamlit
st.set_page_config(page_title="Kiarostami Film Festival Dashboard", layout="wide")

st.title("🎬 Kiarostami Short Film Festival Dashboard")

# 📌 خواندن فایل CSV از GitHub
csv_url = "https://raw.githubusercontent.com/sheydaei/My-projects/main/Kiarostami_film_festival_1/Final_Final2.csv"
df = pd.read_csv(csv_url)

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

# 📌 ایجاد سرور Flask برای اجرای Dash
server = flask.Flask(__name__)
dash_app = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash/")

# 📌 طراحی کامل داشبورد
dash_app.layout = html.Div([
    html.H1("Kiarostami Short Film Festival", style={'textAlign': 'center', 'color': 'rgb(255, 255, 255)'}),  
    
    html.Div([
        html.Div([
            html.H3("Total Participants", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  
            html.H1(f"{df3.shape[0]}", style={'textAlign': 'center', 'color': 'rgb(255, 255, 255)'})  
        ], style={'backgroundColor': 'rgb(0, 0, 0)', 'padding': '20px', 'borderRadius': '10px', 'width': '30%', 'margin': '10px'}),
        
        html.Div([
            html.H3("Total Movies", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  
            html.H1(f"{df.shape[0]}", style={'textAlign': 'center', 'color': 'rgb(255, 255, 255)'})  
        ], style={'backgroundColor': 'rgb(1, 1, 1)', 'padding': '20px', 'borderRadius': '10px', 'width': '30%', 'margin': '10px'})
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),
    
    html.Div([
        html.H2("Gender Breakdown", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  
        dcc.Graph(id='gender-pie-chart', figure=px.pie(df, names='Gender', title='Gender Breakdown', hole=0.4, template="plotly_dark"))
    ]),

    html.Div([
        html.H2("Age Distribution", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  
        dcc.Graph(id='age-histogram')
    ]),
    
    # Section for Total Countries and Country Table
    html.Div([
        # Card for Total Countries
        html.Div([
            html.H3("Total Countries", style={'textAlign': 'center', 'color': 'rgb(168, 182, 203)'}), 
            html.H1(f"{df['Country of Residence'].nunique()}", style={'textAlign': 'center', 'color': 'rgb(255, 255, 255)'})  # سفید
        ], style={
            'backgroundColor': 'rgb(0, 0, 0)',  
            'padding': '20px',
            'borderRadius': '10px',
            'width': '30%',
            'margin': '10px auto',
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'center',
            'alignItems': 'center'
        }),
        
        # Table for Countries
        html.Div([
            html.H2("Countries Represented (Table)", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  # آبی خاکستری
            html.Div(id='country-table')
        ])
    ]),
    
    # Section for Films Inspired by Kiarostami
    html.Div([
        html.H2("Films Inspired by Kiarostami", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  # آبی خاکستری
        dcc.Graph(id="bar-chart"),
        html.Div([
            dcc.RangeSlider(
                id='year-slider',
                min=int(df3["Production Year"].min()),
                max=int(df3["Production Year"].max()),
                value=[int(df3["Production Year"].min()), int(df3["Production Year"].max())],
                marks={int(year): str(year) for year in sorted(df3["Production Year"].unique())},
                step=1
            ),
            html.P("Adjust the slider to filter by Year of Production", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'})  # آبی خاکستری
        ])
    ]),
    
    # Section for Movies by Genre and Rejection Status
    html.Div([
        html.H2("Movies by Genre and Rejection Status", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  # آبی خاکستری
        dcc.Graph(id="genre-bar-chart"),
        html.Div([
            dcc.Dropdown(
                id="rejection-dropdown",
                options=[
                    {"label": "All Movies", "value": "all"},
                    {"label": "Rejected Movies", "value": True},
                    {"label": "Non-Rejected Movies", "value": False}
                ],
                value="all",
                placeholder="Select rejection status",
                clearable=False,
                style={'backgroundColor': 'rgb(1, 1, 1)', 'color': 'rgb(255, 255, 255)'}  
            )
        ], style={'width': '50%', 'margin': '0 auto'})
    ]),
    
    # Section for Rejected vs. Inspired by Kiarostami
    html.Div([
        html.H2("Relationship Between Rejection and Inspiration by Kiarostami", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}), 
        dcc.Graph(id="rejected-inspired-graph")
    ]),
    
    # Section for Film Duration Histogram
    html.Div([
        html.H2("Film Duration Histogram", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  
        dcc.Graph(id="duration-histogram"),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id="genre-filter",
                    options=[{"label": genre, "value": genre} for genre in df3['Film Category'].unique()],
                    value=None,
                    placeholder="Select a Genre",
                    clearable=True,
                    style={'backgroundColor': 'rgb(1, 1, 1)', 'color': 'rgb(255, 255, 255)'}  
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id="rejected-filter",
                    options=[
                        {"label": "All Movies", "value": "all"},
                        {"label": "Accepted Movies", "value": False},
                        {"label": "Rejected Movies", "value": True}
                    ],
                    value="all",
                    placeholder="Select Rejection Status",
                    clearable=False,
                    style={'backgroundColor': 'rgb(1, 1, 1)', 'color': 'rgb(255, 255, 255)'}  
                )
            ], style={'width': '48%', 'display': 'inline-block'})
        ], style={'margin': '10px auto'})
    ])
], style={'backgroundColor': 'rgb(0, 0, 0)', 'color': 'rgb(255, 255, 255)'})

# 📌 اجرای Dash در یک `thread` جداگانه
def run_dash():
    server.run(host="0.0.0.0", port=8050, debug=False, use_reloader=False)

thread = threading.Thread(target=run_dash)
thread.daemon = True
thread.start()

# 📌 نمایش داشبورد در `Streamlit` با `iframe`
st.write("🔹 **Loading Dashboard...**")
time.sleep(3)  # تاخیر کوتاه برای اطمینان از اجرای سرور
st.components.v1.iframe("http://localhost:8050/dash/", height=900)
