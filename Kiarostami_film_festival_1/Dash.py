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
        html.H3("Total Participants", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  
        html.H1(f"{df3.shape[0]}", style={'textAlign': 'center', 'color': 'rgb(255, 255, 255)'})  
    ], style={'backgroundColor': 'rgb(0, 0, 0)', 'padding': '20px', 'borderRadius': '10px', 'width': '30%', 'margin': '10px'}),

    html.Div([
        html.H3("Total Movies", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  
        html.H1(f"{df.shape[0]}", style={'textAlign': 'center', 'color': 'rgb(255, 255, 255)'})  
    ], style={'backgroundColor': 'rgb(1, 1, 1)', 'padding': '20px', 'borderRadius': '10px', 'width': '30%', 'margin': '10px'}),

    html.Div([
        html.H2("Gender Breakdown", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  
        dcc.Graph(id='gender-pie-chart')
    ]),

    html.Div([
        html.H2("Age Distribution", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  
        dcc.Graph(id='age-histogram')
    ]),

    html.Div([
        html.H2("Films Inspired by Kiarostami", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  
        dcc.Graph(id="bar-chart"),
        dcc.RangeSlider(
            id='year-slider',
            min=int(df3["Production Year"].min()),
            max=int(df3["Production Year"].max()),
            value=[int(df3["Production Year"].min()), int(df3["Production Year"].max())],
            marks={int(year): str(year) for year in sorted(df3["Production Year"].unique())},
            step=1
        )
    ]),

    html.Div([
        html.H2("Movies by Genre and Rejection Status", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  
        dcc.Graph(id="genre-bar-chart"),
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
    ]),

    html.Div([
        html.H2("Film Duration Histogram", style={'textAlign': 'center', 'color': 'rgb(167, 183, 203)'}),  
        dcc.Graph(id="duration-histogram"),
    ])
], style={'backgroundColor': 'rgb(0, 0, 0)', 'color': 'rgb(255, 255, 255)'})

# 📌 اضافه کردن `Callbacks` برای آپدیت داشبورد
@dash_app.callback(
    dash.Output('age-histogram', 'figure'),
    dash.Input('age-histogram', 'id')  
)
def update_histogram(_):
    fig = px.histogram(df, x="Age", title="Age Distribution", template="plotly_dark")
    return fig

@dash_app.callback(
    dash.Output('gender-pie-chart', 'figure'),
    dash.Input('gender-pie-chart', 'id')
)
def update_pie_chart(_):
    fig = px.pie(df, names='Gender', title='Gender Breakdown', hole=0.4, template="plotly_dark")
    return fig

@dash_app.callback(
    dash.Output("bar-chart", "figure"),
    [dash.Input("year-slider", "value")]
)
def update_bar_chart(selected_year_range):
    filtered_df = df3[
        (df3["Production Year"] >= selected_year_range[0]) &
        (df3["Production Year"] <= selected_year_range[1])
    ]
    fig = px.bar(
        filtered_df,
        x="Production Year",
        y=filtered_df.groupby("Production Year").size(),
        title="Movies Inspired by Kiarostami Over the Years",
        template="plotly_dark"
    )
    return fig

# 📌 اجرای Dash در یک `thread` جداگانه
def run_dash():
    server.run(host="0.0.0.0", port=8050, debug=False, use_reloader=False)

thread = threading.Thread(target=run_dash)
thread.daemon = True
thread.start()

# 📌 نمایش داشبورد در `Streamlit` با `iframe`
st.write("🔹 **Loading Dashboard...**")
time.sleep(3)  
st.components.v1.iframe("http://localhost:8050/dash/", height=900)
