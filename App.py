
# load census data

import pandas as pd
census_data_all = pd.read_csv("assets/census_data_all.csv")

census_data_all['PopTotalv2'] = 2 * census_data_all['PopulationTotal']



# load geojson

import json

with open("assets/geo_zones.json") as f:
    geo_zones = json.load(f)



import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# css style
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
app.title = "OpenGeoKPI"
server = app.server

# navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Navbar Simple",
    brand_href="#",
    color="secondary",
    dark=True,
)

# scale selection


scale_selection_text = html.P(
    'Select Scale:',
    style={
        'font-size': '120%',
        'margin-bottom': '15px',
        'margin-top': '15px',
        'margin-left': '5%'
    }
)

dropdown_scale = dcc.Dropdown(
    id='scale',
    options=[
        {'label': 'Municipality', 'value': 'Municipality'},
        {'label': 'Region', 'value': 'Region'}
    ],
    value='Region',
    style={
        'width': '90%',
        # 'width': '400px',
        'margin-left': '2%'}
)

# kpi selector

kpi_selection_text = html.P(
    'Select KPI:',
    style={
        'font-size': '120%',
        'margin-bottom': '15px',
        'margin-top': '15px',
        'margin-left': '5%'
    }
)

dropdown_kpi = dcc.Dropdown(
    id='kpi',
    # options=[{'label': i, 'value': i} for i in communes_list],
    options=[
        {'label': 'Population', 'value': 'PopulationTotal'},
        {'label': 'Population v2', 'value': 'PopTotalv2'}
    ],
    # value='PopulationTotal',
    style={
        'width': '90%',
        'margin-left': '2%'
    }
)

# body

body = dbc.Container([
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            scale_selection_text
                        ),
                        dbc.Row(
                            dropdown_scale
                        ),
                        dbc.Row(
                            kpi_selection_text
                        ),
                        dbc.Row(
                            dropdown_kpi
                        )
                    ],
                    md=4
                ),
                dbc.Col(
                    dcc.Graph(id='map_communes'),
                    md=8
                )
            ]
        )
    ],
    className="mt-2",
    fluid=True
)

app.layout = html.Div([navbar, body])


@app.callback(
    Output('map_communes', 'figure'),
    [
        Input('scale', 'value'),
        Input('kpi', 'value'),
     ]
)
def update_map_kpi(scale, kpi):
    data = census_data_all[census_data_all['Level'] == scale]
    fig = px.choropleth_mapbox(data,
                               geojson=geo_zones,
                               color=kpi,
                               locations="Code", featureidkey="properties.Code",
                               center={"lat": 48.8534, "lon": 2.3488},
                               mapbox_style="carto-positron", zoom=7, height=600)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


app.run_server(debug=False, use_reloader=False)