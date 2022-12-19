# -*- coding: utf-8 -*-
from dash import Dash, dcc, html, Input, Output
from flats_to_map import flats_to_map
import dash_bootstrap_components as dbc

from project_python.banki_parser.start_scrapper import get_banks


app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server

ALLOWED_CHOICE = (
    "initialFee", "salary"
)
button = html.Div(
    [
        dcc.Input(id="fee", type="number", placeholder="initialFee"),
        dcc.Input(
            id="salary", type="number", placeholder="salary",
        ),
        html.Hr(),
        html.Div(id="number-out"),
    ]
)


app.layout = html.Div([
    html.H1('Квартиры в Москве и МО'),
              dcc.RadioItems(
                id='pages',
                options=['1-100', '101-200', '201-300',
                         '301-500', '501-700', '701-800',
                         '801-1000', '1001-1200', '1201-1300'],
                value='1-100',
                inline=True
            ),
    button,
    html.Iframe(id='map', srcDoc=open('map.html', 'r', encoding='utf-8').read(), width='100%', height='600')
])

PAYLOAD = {
    'fee': 2_000_000,
    'salary': 30_000,
    'child': True,
}

@app.callback(
    Output("number-out", "children"),
    Input("fee", "value"),
    Input("salary", "value"),
)
def number_render(fee, salary):
    PAYLOAD['fee'] = int(fee)
    PAYLOAD['salary'] = int(salary)
    return "initialFee: {}, salary: {}".format(fee, salary)


@app.callback(
    Output("map", "srcDoc"),
    Input("pages", "value"))
def display_choropleth(pages):
    flats_to_map(str(pages), [1, 1, 1])

    fig = open('map.html', 'r', encoding='utf-8').read()

    return fig


@server.route('/mortgage/<int:price>')
def mortgage(price):
    return get_banks(price, PAYLOAD['fee'], True, 'new', PAYLOAD['salary'])


if __name__ == '__main__':
    app.run_server()
