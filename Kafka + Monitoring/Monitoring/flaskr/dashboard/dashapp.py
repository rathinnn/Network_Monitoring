import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.express as px
#import findspark
#findspark.init()
from pyspark.sql import SparkSession

import plotly.graph_objs as go
from dash.dependencies import Input, Output

from Monitoring.flaskr.plots.mapPlot import updateMap
from Monitoring.flaskr.plots.graphPlot import updateMethod, updateStatus, updateSearch, updateTotal, updateBlocked
from Monitoring.flaskr.SparkJobs import init, getMapDF, getStatusDF, getSearchDF, getBlockedDF, getMethodDF

def init_dashboard(server):

    ACCESS_TOKEN = open(".mapbox_token").read()


    spark = SparkSession.builder.appName("local").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    init(spark)
    mapdf = getMapDF(spark)
    statusdf = getStatusDF(spark)
    searchdf = getSearchDF(spark)
    blockedf = getBlockedDF(spark)
    methoddf = getMethodDF(spark)




    CONTENT_STYLE = {
        'margin-left': '5%',
        'margin-right': '5%',
        'padding': '20px 10p'
    }

    TEXT_STYLE = {
        'textAlign': 'center',
        'color': '#191970'
    }

    CARD_TEXT_STYLE = {
        'textAlign': 'center',
        'color': '#0074D9'
    }





    row1 = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='method'), md=4
            ),
            dbc.Col(
                dcc.Graph(id='status'), md=4
            ),
            dbc.Col(
                dcc.Graph(id='search'), md=4
            ),
            html.Div([dcc.Interval(id = 'update',interval = 20000,n_intervals = 0)])
        ]
    )

    row2 = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='map'), md=12,
            )
        ]
    )

    row3 = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='total'), md=6
            ),
            dbc.Col(
                dcc.Graph(id='blocked'), md=6
            )
        ]
    )

    content = html.Div(
        [
            html.H2('DashBoard', style=TEXT_STYLE),
            html.Hr(),
            row1,
            row2,
            row3
        ],
        style=CONTENT_STYLE
    )

    app = dash.Dash(server = server,requests_pathname_prefix="/spark/",external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div([content])

    @app.callback([Output("map", "figure") , Output("method", "figure") , Output("status", "figure"), Output("search", "figure"), Output("total", "figure"), Output("blocked", "figure")],[Input("update", "n_intervals")])
    def update(n_intervals):
        totaldf = mapdf.select("*").toPandas()
        #searchdf.show()
        return updateMap(go,totaldf,px,ACCESS_TOKEN), updateMethod(px,methoddf.select("*").toPandas()) , updateStatus(px,statusdf.select("*").toPandas()), updateSearch(px, searchdf.select("*").toPandas()),  updateTotal(px, totaldf) , updateBlocked(px,blockedf.select("*").toPandas())

    return app





