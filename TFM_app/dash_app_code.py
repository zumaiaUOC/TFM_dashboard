
from multiprocessing.connection import Client
from signal import siginterrupt
import dash
from dash.dependencies import Output, Input
from dash import dcc, html, dash_table, callback, Dash
import plotly.graph_objs as go
import pandas as pd
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

from dash.dash_table.Format import Format, Group, Scheme
from dash.dash_table import FormatTemplate


from datetime import datetime
import pandas as pd
import glob
import os
import plotly.express as px
import json

#from django_app.calculos import *

from datetime import datetime as dt

from .etl_data import *


####################################################################################################
####################################################################################################
##                                                        ##########################################
####################################################################################################
####################################################################################################


print('1200')


your_path = 'media/data/'
files = os.listdir(your_path)

external_stylesheets = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"


# Important: Define Id for Plotly Dash integration in Django
app_exploratory_data_analysis = DjangoDash('dash_exploratory_data_analysis_id')

app_exploratory_data_analysis.css.append_css({
    "external_url": external_stylesheets
})

print('1300')


plot_missing_values()
print('1300.1')
pie_plot_machine_status()
print('1300.2')
plot_sensors()
print('1300.3')
corr_heat_map()
print('1301')
df = html_table_descripcion()
df_datos = melt_data()
#df_datos_clean = data_clean_df()
print('1302')
#evolucion()
app_exploratory_data_analysis.layout = html.Div([

    html.Div([
        html.Div([
            html.H1('EDA- Exploratory Data Analysis',
                    style={'color': '#ffffff', 'font-size': '30px', 'font-weight': 'bold', 'text-align': 'center'}),

            

        ], className="two-third column", id='title1'),


    html.Div([

        html.Div([
            html.H4(children='Registoros/Filas',
                    style={
                        'textAlign': 'center',
                        'color': 'black'}
                    ),

            html.P(f"{registros()}",
                   style={
                       'textAlign': 'center',
                       'color': 'black',
                       'fontSize': 30}
                   ),
            dbc.Card(
                [dbc.CardImg(),

                 dbc.CardBody(
                    [
                        html.P(
                            'Aquí mostramos el número de filas que hay en el dataset original.',
                            className="card-text"),
                        html.P(
                            "El valor es: " + str(registros()) + " filas",
                            className="card-text",
                            id='card-text',
                        ),
                    ]), ], ),

        ], className="card_container three columns",
        ),


        html.Div([
            html.H4(children='Columnas/Variables',
                    style={
                        'textAlign': 'center',
                        'color': 'black'}
                    ),

            html.P(f"{variables()}",
                   style={
                       'textAlign': 'center',
                       'color': 'black',
                       'fontSize': 30}
                   ),
            dbc.Card(

                [dbc.CardImg(),

                 dbc.CardBody(
                    [
                        html.P(
                            'Aquí mostramos el número de variables o columnas que compone el dataset original.',
                            className="card-text"),
                        html.P(
                            "El valor es: " +
                            str(variables()) + " variables",
                            className="card-text",
                            id='card-text',
                        ),
                    ]), ],),

        ], className="card_container three columns",
        ),


        html.Div([
            html.H4(children='Sensores',
                    style={
                        'textAlign': 'center',
                        'color': 'black'}
                    ),

            html.P(f"{sensores()}",
                   style={
                       'textAlign': 'center',
                       'color': 'black',
                       'fontSize': 30}
                   ),
            dbc.Card(

                [dbc.CardImg(),
                 dbc.CardBody(
                    [
                        html.P(
                            'Aquí indicamos el número de sensores utilizados. Aquí se han eliminado la columna id, timestamp y machine_status.',
                            className="card-text"),
                        html.P(
                            "El valor es: " + str(sensores()) + " sensores.",
                            className="card-text",
                            id='card-text',
                        ),
                    ]), ],),

        ], className="card_container three columns",
        ),

        html.Div([
            html.H4(children='Missing Values',
                    style={
                        'textAlign': 'center',
                        'color': 'black'}
                    ),

            html.P(f"{missing_values()}" + ' valores',
                   style={
                       'textAlign': 'center',
                       'color': 'black',
                       'fontSize': 30}
                   ),
            dbc.Card(

                [dbc.CardImg(),
                 dbc.CardBody(
                    [
                        html.P(
                            "En este apartado mostramos el número de missing values que hay en el dataset original. Destacamos:  \
                            sensor_15    220320, \
                            sensor_50     77017, \
                            sensor_51     15383, \
                            sensor_00     10208, \
                            sensor_07      5451",
                            className="card-text"),
                        html.P(
                            "El total de valores perdidos es de: " + str(missing_values()),
                            className="card-text",
                            id='card-text',
                        ),
                    ]), ],),

        ], className="card_container three columns",

        ),


    ], className="row flex-display"),
    
    
    html.Div([

        

        html.Div([
            html.H4(children='Cuadro resumen descripción del dataset',
                    style={
                        'textAlign': 'center',
                        'color': 'black'}
                    ),

            dbc.Container(children=[
                dbc.Label('Estadísticas Descriptivas:',
                          style={
                              'textAlign': 'center',
                              'color': 'black'}),
                dash_table.DataTable(df.to_dict('records'), [
                    {"name": i, "id": i} for i in df.columns], id='tbl'),
                dbc.Alert(id='tbl_out', 
                          style={'backgroundColor': '#eeeeee' , 
                                 'border-color': '#eeeeee'}),
            ]),

        ], className="card_container eleven columns",
        ),


    ], className="row flex-display"),
    
    
    
    
    html.Div([

        html.Div([
            html.H4(children='Mapa Calor de Missing Values',
                    style={
                        'textAlign': 'center',
                        'color': 'black'}
                    ),


            dbc.Card(

                [dbc.CardImg(
                    src="/static/graficas/missing.png", top=True),

                 dbc.CardBody(
                    [
                        html.P(
                            "Factores como el clima, el mál funcionamiento eléctrico, mantenimiento, fallos humanos, etc. \
                                pueden ser los responsables de una gran cantidad de casos en que varios de los sensores no registran al mismo tiempo.\
                            \
                            Puesto que puede ser un indicador de el sistema no funciona, vamos a apartarlo y tratar los valores que faltan más adelante. \
                            Actualmente tenemos dos opciones para tratar los valores que faltan: \
	                        1º. Eliminar el resto de las filas en las que faltan valores. \
	                        2º. Rellenar los valores que faltan.",
                            className="card-text",
                            id='card-text',
                        ),
                    ]), ],),

        ], className="card_container eleven columns",
        ),


    ], className="row flex-display"),
    

    
    html.Div([

        html.Div([
            html.H4(children='Distribución de la situación de la máquina',
                    style={
                        'textAlign': 'center',
                        'color': 'black'}
                    ),
            dbc.Card(
                [dbc.CardImg(
                    src="/static/graficas/pie_machine_status.png", top=True),
                 dbc.CardBody(
                    [
                        html.P(
                            "Como podemos ver, la mayoría de las veces los sensores registran NORMAL. \
                                Esto tiene sentido porque la bomba debería estar funcionando normalmente la mayor parte del tiempo. \
                                    El siguiente grupo es el de RECUPERACIÓN, que también tiene sentido dado que la máquina se rompe y tarda un poco en recuperarse. \
                                        Por último, sólo el 0,004% de los datos está en estado ROTURA. \
                            Esto está bien porque una máquina se rompe y, en teoría, no debería estar rota mucho tiempo.",
                            className="card-text",
                            id='card-text',
                        ),
                    ]), ],),
        ], className="card_container eleven columns",
        ),
    ], className="row flex-display"),    
    
    html.Div([

        html.Div([
            html.H4(children='Distribución de la situación de la máquina',
                    style={
                        'textAlign': 'center',
                        'color': 'black'}
                    ),
            dbc.Card(
                [dbc.CardImg(
                    src="/static/graficas/corr_heatmap.png", top=True),
                 dbc.CardBody(
                    [
                        html.P(
                            "Hemos creado 2 nuevas columnas, llamadas stat y rol. \
                            Stat está creado mapeando machine_status {'NORMAL': 1, 'RECOVERING': 0.5, 'BROKEN': 0} \
                            Rol es un rolling mean de stat, con el fin de poder visualizar mejor las roturas de actividad.\n \
                                \
                            Por último hemos seleccionado las variables que tengan una correlación entre los sensores y stat superior a 0.75.\n \
                            Los sensores seleccionados son: \n \
                            ['sensor_02', 'sensor_04', 'sensor_06', 'sensor_10', 'sensor_11', 'sensor_12']",
                            className="card-text",
                            id='card-text',
                        ),
                    ]), ],),
        ], className="card_container eleven columns",
        ),
    ], className="row flex-display"),  
        
    
], id="mainContainer", style={"display": "flex", "flex-direction": "column"
                              }),
], className="container")




############################################################################################
#### VISUALIZACIÓN DE LOS DATOS EN EL NAVEGADOR ############################################
#

app_visualizacion = DjangoDash('dash_visualizacion_id')

app_visualizacion.css.append_css({
    "external_url": external_stylesheets
})

app_visualizacion.layout = html.Div([

    html.Div([
        html.Div([
            html.H1('Visualización de los datos recogidos por los sensores',
                    style={'color': '#ffffff', 'font-size': '35px', 'font-weight': 'bold', 'text-align': 'center'}),
        ], className="two-third column", id='title1'),
        
        html.Div([
            html.H4('Leyenda:  La cruz roja indica la rotura de la máquina \n \
                En color amarillo se muestran el periodo de recuperación de la máquina \n \
                    y en color gris es el periodo de funcionamiento normal de la máquina.',
                    style={'color': '#ffffff', 'font-size': '20px', 'font-weight': 'bold', 'text-align': 'center'}),
        ], className="two-third column", id='title1'),

    
    

    
    html.Div([

        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_01.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_02.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_03.png", top=True),
                 ],),], className="card_container eleven columns",),

        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_04.png", top=True),
                 ],),], className="card_container eleven columns",),
                       
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_05.png", top=True),
                 ],),], className="card_container eleven columns",),
                 
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_06.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_07.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_08.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_09.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_10.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_11.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_12.png", top=True),
                 ],),], className="card_container eleven columns",),

        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_13.png", top=True),
                 ],),], className="card_container eleven columns",),
                
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_14.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_16.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_17.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_18.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_19.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_20.png", top=True),
                 ],),], className="card_container eleven columns",),

        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_21.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_22.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_23.png", top=True),
                 ],),], className="card_container eleven columns",),
                
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_24.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_25.png", top=True),
                 ],),], className="card_container eleven columns",),
                 
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_26.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_27.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_28.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_29.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_30.png", top=True),
                 ],),], className="card_container eleven columns",),

        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_31.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_32.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_33.png", top=True),
                 ],),], className="card_container eleven columns",),

        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_34.png", top=True),
                 ],),], className="card_container eleven columns",),
                         
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_35.png", top=True),
                 ],),], className="card_container eleven columns",),
                 
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_36.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_37.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_38.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_39.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_40.png", top=True),
                 ],),], className="card_container eleven columns",),

        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_41.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_42.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_43.png", top=True),
                 ],),], className="card_container eleven columns",),

        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_44.png", top=True),
                 ],),], className="card_container eleven columns",),
                         
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_45.png", top=True),
                 ],),], className="card_container eleven columns",),
                 
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_46.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_47.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_48.png", top=True),
                 ],),], className="card_container eleven columns",),
        
        
        
        html.Div([
            dbc.Card([dbc.CardImg(
                    src="/static/graficas/sensor_49.png", top=True),
                 ],),], className="card_container eleven columns",),

        html.Div([
            
            html.H4('Las 2 últimas gráficas no corresponden a sensores.',
                    style={'color': '#000000', 'font-size': '20px', 'font-weight': 'bold', 'text-align': 'center'}),
            
            html.H4('Stat está creado mapeando machine_status: {"NORMAL": 1, "RECOVERING": 0.5, "BROKEN": 0}.  \
                    Rol es un rolling mean de stat, con el fin de poder visualizar mejor las roturas de actividad.',
            style={'color': '#000000', 'font-size': '20px', 'font-weight': 'bold', 'text-align': 'center'}),
        ], className="card_container eleven columns", id='title1'),

        html.Div([
            dbc.Card([dbc.CardImg(
                src="/static/graficas/stat.png", top=True),
            ],), ], className="card_container eleven columns",),

        html.Div([
            dbc.Card([dbc.CardImg(
                src="/static/graficas/rol.png", top=True),
            ],), ], className="card_container eleven columns",),
                                           
        

    ], className="row flex-display"),    
        
    
], id="mainContainer", style={"display": "flex", "flex-direction": "column"
                              }),
], className="container")



###############################################
###############################################

# Important: Define Id for Plotly Dash integration in Django
app_datos = DjangoDash('datos_id')

app_datos.css.append_css({
    "external_url": external_stylesheets
})

print('DATOS')
print(df_datos.head(5))
print(df_datos.info())
df_datos.set_index('timestamp', inplace=True)

names = df_datos.columns
print(names)

app_datos.layout = html.Div(
    [
        html.Div([
            dcc.Dropdown(
                id='ddl_x',
                options=[{'label': i, 'value': i} for i in names],
                value='sensor_02',
                style={'width':'50%'}
            ),
            dcc.Dropdown(
                id='ddl_y',
                options=[{'label': i, 'value': i} for i in names],
                value='sensor_04',
                style={'width':'50%'}
            ),
        ],style={'width':'100%','display':'inline-block'}),
        html.Div([
            dcc.Graph(id='graph1') 
        ],style={'width':'100%','display':'inline-block'})
    ]
)
@app_datos.callback(
    Output(component_id='graph1', component_property='figure'),
    [
        Input(component_id='ddl_x', component_property='value'),
        Input(component_id='ddl_y', component_property='value')
    ]
)
def update_output(ddl_x_value, ddl_y_value):
    figure={
        'data': [
            go.Scatter(
                x=df_datos[df_datos['machine_status'] == cls][ddl_x_value],
                y=df_datos[df_datos['machine_status'] == cls][ddl_y_value],
                mode='markers',
                marker={ 'size': 15 },
                name=cls
            ) for cls in df_datos['machine_status'].unique()
        ],
        'layout': 
            go.Layout(
                height= 650,
                hovermode= 'closest',
                title=go.layout.Title(text='Comparativa entre sensore principales',xref='paper', x=0),
                xaxis={'title':ddl_x_value},
                yaxis={'title':ddl_y_value},
            )
        
    }
    return figure
