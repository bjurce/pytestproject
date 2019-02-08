# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Title: Customer Map on demographics Data solutions for Exercise 3 (Tabs)
Author: Patrick Glettig
Date: 17.11.2018
"""
# import os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import dash_table

#os.chdir('C:/Users/patri/Dropbox/Python Advanced - Slides & Code/data')

demographics = pd.read_csv('data/demographics.csv')
demographics["Birthdate"] = pd.to_datetime(demographics["Birthdate"],
                                            format="%d.%m.%Y",
                                            utc=True,
                                            dayfirst=True)

demographics["JoinDate"] = pd.to_datetime(demographics["JoinDate"],
                                            format="%d.%m.%Y",
                                            utc=True,
                                            dayfirst=True)

gender_options = []
for gender in demographics['Gender'].unique():
    gender_options.append({'label':str(gender),
                           'value':gender})


app = dash.Dash()
# add birthdate picker
from datetime import datetime as dt
import dash
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt(1995, 8, 5),
        max_date_allowed=dt(2017, 9, 19),
        initial_visible_month=dt(2017, 8, 5),
        end_date=dt(2017, 8, 25)
    ),
    html.Div(id='output-container-date-picker-range')
])


@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix


if __name__ == '__main__':
    app.run_server(debug=True)
#Add the CSS Stylesheet
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.layout = html.Div([html.H1('Customer Map', style={'textAlign':'center'}),
                       html.Div(children=[html.Div([html.H3('Inputs'),
                                                   html.H6('Gender'),
                                                   html.P(
                                                           dcc.Checklist(id='gender-picker',
                                                                         options=gender_options,
                                                                         values=['m','f','alien']
                                                                         )
                                                           ),
                                                    html.H6('Join Date'),
                                                    html.P(
                                                            dcc.DatePickerRange(
                                                                    id='date-picker-range',
                                                                    min_date_allowed=min(demographics.JoinDate),
                                                                    max_date_allowed=max(demographics.JoinDate),
                                                                    initial_visible_month=dt(1989, 11, 9),
                                                                    start_date=min(demographics.JoinDate),
                                                                    end_date=max(demographics.JoinDate)
                                                                    )
                                                            )
                                                    ])
                                            ],
                                style = {'float':'left'},
                                className = "two columns"),
                        html.Div([dcc.Tabs(children=[dcc.Tab(label='Map',
                                                            children=html.Div([
                                                                    dcc.Graph(id='CustomerMap')
                                                                    ])
                                                            ),
                                                    dcc.Tab(label='Data',
                                                            children=[html.Div([dash_table.DataTable(
                                                                                id='table',
                                                                                columns = [{"name": i, "id": i} for i in demographics.columns],
                                                                                data = demographics.to_dict("rows")
                                                                )])
                                                                    ]
                                                            )
                                                    ]
                                            )
                                ],
                                className = "nine columns",
                                style = {'float':'right'})
                ]
                )

@app.callback(
    dash.dependencies.Output('CustomerMap', 'figure'),
    [dash.dependencies.Input('gender-picker', 'values'),
     dash.dependencies.Input('date-picker-range', 'join_start_date'),
     dash.dependencies.Input('date-picker-range', 'join_end_date')])

def update_figure(selected_gender, start_date, end_date):    
     filtered_df = demographics.loc[(demographics['Gender'].isin(selected_gender)) &  
                                  (demographics['JoinDate'] >= start_date) &
                                  (demographics['JoinDate'] <= end_date) ,]
     zip_size = demographics.groupby(["zip_city"]).size()
    
     zip_size = demographics.groupby(["zip_city", 'zip_longitude', 'zip_latitude']).size()
    
     zipcity = zip_size.index.get_level_values("zip_city").tolist() 
     customerCount = zip_size.values.tolist()
     
     hovertext = []
     for i in range(len(customerCount)):
          k = str(zipcity[i]) + ':' + str(customerCount[i])
          hovertext.append(k)    #only the updated arguments are returned to the figure object, not a figure object itself.
     
     return {'data':[dict(
                        type = 'scattergeo',
                        locationmode = 'USA-states',
                        lon = zip_size.index.get_level_values("zip_longitude").tolist(),
                        lat = zip_size.index.get_level_values("zip_latitude").tolist(),
                        text = hovertext,
                        hoverinfo = 'text',
                        marker = dict(
                        size = customerCount,
                        line = dict(width=0.5, color='rgb(40,40,40)'),
                        sizemode = 'area'
                        )
                        )
                    ]
            }

#We need another App Callback
    
@app.callback(
    dash.dependencies.Output('table', 'data'),
    [dash.dependencies.Input('gender-picker', 'values'),
     dash.dependencies.Input('date-picker-range', 'join_start_date'),
     dash.dependencies.Input('date-picker-range', 'join_end_date')])

def update_table(selected_gender, start_date, end_date):    
    filtered_df = demographics.loc[(demographics['Gender'].isin(selected_gender)) &  
                                  (demographics['JoinDate'] >= join_start_date) &
                                  (demographics['JoinDate'] <= join_end_date), ]
    return filtered_df.to_dict("rows")

if __name__ == '__main__':
    app.run_server()
