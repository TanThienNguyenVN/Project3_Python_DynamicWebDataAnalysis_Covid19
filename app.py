from flask import Flask, render_template, request

import pandas as pd
import numpy as np
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from Covid19Data import totalCovidConfirmCase, medianAge, dailyCasebyAge, dailyHospitalbyAge, pctHospitalPerCase, relationHospitalCase

# Get data
Covid_Tan = pd.read_csv("Covid_Tan.csv", parse_dates = ["StatisticsProfileDate"])
age_group = Covid_Tan.Age.unique()

# Create one new dataset for graphing the Percentage of Total Hospitalised Cases per Total Confirmed Cases by Age
Covid_Tan_max = Covid_Tan[Covid_Tan.StatisticsProfileDate == Covid_Tan.StatisticsProfileDate.max()].copy()
Covid_Tan_max["HospitalisedPercentagePerCase"] = Covid_Tan_max.HospitalisedCases * 100/Covid_Tan_max.Cases

# Create a new dataset to show the relationship between Hospitalised Cases Percentage and Confirmed Cases Percentage in all Age Group
Covid_Tan_max["Hospitalised"] = Covid_Tan_max.HospitalisedCases * 100/Covid_Tan_max.HospitalisedCovidCases
Covid_Tan_max["Confirmed Cases"] = Covid_Tan_max.Cases * 100/Covid_Tan_max.CovidCasesConfirmed

Covid_Tan_new = Covid_Tan_max.loc[:,["Age","Confirmed Cases","Hospitalised"]].copy()
Covid_Tan_new_melt = pd.melt(Covid_Tan_new, id_vars="Age",value_name="Percentage %",var_name="Type")

 
# App 
app = dash.Dash(__name__)
app.title = "Covid-19 Statistics Dashboard"

# Graph section 
Graph1 = html.Div(children = [html.Div(children = [
                            dcc.Graph(id = "totalCovidConfirmCase")       #graph only requireds unique id in our case
                                    ],
                            style = {'width': '45%', "left": "5%",
                                     'display': 'inline-block', "background-color": "#282828",
                                    }
                                    ),
                            html.Div(children = [
                                dcc.Graph(id = "medianAge") #graph only requireds unique id in our case
                                ],
                            style = {'width': '50%', "left": "55%",
                                 'display': 'inline-block', "background-color": "#282828"
                                }),
                                
                        ]
                        )
Graph2 = html.Div(children = [html.Div(children = [
                                dcc.Graph(id = "dailyCasebyAge") #graph only requireds unique id in our case
                                ],
                            style = {'width': '45%',  "left": "5%",
                                 'display': 'inline-block', "background-color": "#282828"
                                }),
                        
                        html.Div(children = [
                                dcc.Graph(id = "dailyHospitalbyAge") #graph only requireds unique id in our case
                                ],
                        style = {'width': '45%', "left": "55%",
                                 'display': 'inline-block', "background-color": "#282828"
                                })
                        ]
                        )

Graph3 = html.Div(children = [html.Div(children = [
                                dcc.Graph(id = "pctHospitalPerCase") #graph only requireds unique id in our case
                                ],
                            style = {'width': '45%',  "left": "5%",
                                 'display': 'inline-block', "background-color": "#282828"
                                }),
                        
                        html.Div(children = [
                                dcc.Graph(id = "relationHospitalCase") #graph only requireds unique id in our case
                                ],
                        style = {'width': '50%', "left": "55%",
                                 'display': 'inline-block', "background-color": "#282828"
                                })
                        ]
                        )
                        
# App Layout 
app.layout = html.Div(children=[
    html.Div([
    html.Img(src=app.get_asset_url('datagove.png'), style ={"height": "35px","width":"180px", "margin-top":"30px"}, className = 'two columns'),
    html.Div([
    html.H2("COVID-19 HPSC Detailed Statistics by Age Groups", style={'color' :'#00008B','textAlign':'center'}),
    html.H4("Statistics Date (02/03/2020 - 21/12/2021)", style={'color' :'#454545','textAlign':'center'}
    )], className = 'eight columns'),
    html.Img(src=app.get_asset_url('itcarlow_logo_2020.png'), style ={"height": "80px","width":"180px", "margin-top":"20px"}, className = 'two columns')
    ], className = 'row'),
    html.Div([
    html.Div(html.H3("Age Group Selection", style={'color' :'#800000'})),
    html.Div(dcc.Checklist(
        id="checklist",
        options=[{"label": x, "value": x} 
                 for x in age_group],
        value=age_group[:],
        labelStyle={'display': 'inline-block'}
    )
    )
    ], className = 'twelve columns'),
    html.Div(Graph1, className = 'twelve columns'),
    html.Div(Graph2, className = 'twelve columns'),
    html.Div(Graph3, className = 'twelve columns'),
    html.Div(html.H4("Copyright (c) 2022 by Tan Thien Nguyen", style={'color' :'#454545','textAlign':'center'}), className = 'twelve columns')
])

# App Callback

@app.callback([Output(component_id = "totalCovidConfirmCase", component_property = "figure"),
               Output(component_id = "medianAge", component_property = "figure"),
               Output(component_id = "dailyCasebyAge", component_property = "figure"),
               Output(component_id = "dailyHospitalbyAge", component_property = "figure"),
               Output(component_id = "pctHospitalPerCase", component_property = "figure"),
               Output(component_id = "relationHospitalCase", component_property = "figure")],               
               [Input(component_id = "checklist", component_property = "value")]
             )
def the_callback_function(ages):
    fig1 = totalCovidConfirmCase(ages)
    fig2 = medianAge()
    fig3 = dailyCasebyAge(ages)
    fig4 = dailyHospitalbyAge(ages)
    fig5 = pctHospitalPerCase(ages)
    fig6 = relationHospitalCase(ages) 
    return fig1, fig2, fig3, fig4, fig5, fig6
    
if __name__ == "__main__":
    app.run_server(debug=True)
