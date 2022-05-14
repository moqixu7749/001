import pandas as pd 
import plotly.graph_objects as go 
import dash
import dash_html_components as html 
import dash_core_components as dcc 
from dash.dependencies import Input, Output
import plotly.express as px 
# read the data 
airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', encoding="ISO-8859-1",dtype={'Div1Airport':str,'Div1TailNum':str,'Div2Airport':str,'Div2TailNum':str})

#create a dash application
app=dash.Dash()

#build the dash layout
app.layout=html.Div(children=[html.H1('Flight DelayTime Statistics',
                    style={'textAlign':'center','color':'#503D36',
                    'font-size':30}),
                    html.Div(["Input Year:",dcc.Input(id='input-year',value='2010',
                    type='number',style={'height':'35px','font-size':30}),],
                    style={'font-size':30}),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Div(dcc.Graph(id='carrier-plot')),
                        html.Div(dcc.Graph(id='weather-plot'))
                        ],
                        style={'display':'flex'}),
                    html.Div([
                        html.Div(dcc.Graph(id='nas-plot')),
                        html.Div(dcc.Graph(id='security-plot'))
                        ],style={'display':'flex'}),
                        html.Div(dcc.Graph(id='late-plot'),style={'width':'65%'})
                        ])

""" Compute_info function description
this function takes in airplane data and select
year as an input and performs computation for 
creating charts and plots.

Arguments: 
    airline_data:Input airline data.
    entered_year: Input year for which computation needs
                  to be performed.
Returns:
    computed averaged dataframes for carries delay,
    weather delay, NAS delay, security delay , and 
    late aircraft delay.

"""
def compute_info(airline_data, entered_year):
    # select data 
    avg_car=df.groupby(['Month','Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather=df.grouby(['Month','Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS=df.groupby(['Month','Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec=df.groupby(['Month','Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late=df.groupby(['Month','Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late

# callback decorator
@app.callback([
    Output(component_id='carrier-plot',component_property='figure'),
    Output(component_id='weather-plot',component_property='figure'),    
    Output(component_id='nas-plot',component_property='figure'),        
    Output(component_id='sec-plot',component_property='figure'),        
    Output(component_id='late-plot',component_property='figure')

],
    Input(component_id='inut-year',component_property='value'))
# Computation to callback function and return graph
def get_graph(entered_year):

# Compute required infomation for creating the graph from the data
   avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(airline_data, entered_year)
#line plot for carrier delay 
   carrier_fig=px.line(avg_car,x='Month',y='CarrierDelay',color='Reporting_Airline',title='Average Carried delay time(min) by Airline')
#line plot for weather delay
   weather_fig=px.line(avg_weather,x='Month',y='weatherDelay',color='Reporting_Airline',title='Average Weath. Delay time(min) by AirLine')
#line plot of nas delay 
   nas_fig=px.line(avg_nas,x='Month',y='NASDelay',color='Reporting_Airline',title='Average NAS dealy time(min) by  Airline')
#line plot for security delay 
   sec_fig=px.line(avg_sec,x='Month',y='SecDelay',color='Reporting_Airline',title='Average Security Delay Time(min) by AirL')
#line plot for late  delay
   late_fig =px.line(avg_late,x='Month',y='LateDelay',color='Reporting_Airline',title='Average_lateDelay Time(min) by AirLine')

# Run the app
if __name__=='__main__':
    app.run_server()
