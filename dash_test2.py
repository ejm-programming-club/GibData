import os
import json
import dash
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from questions import Questions


s_path = os.path.dirname(__name__)
s_path_data = os.path.join(s_path, "data")

s_cached_data_fname = os.path.join(s_path_data, 'cached_data.json')

with open(s_cached_data_fname) as f:
    Q_ib2018 = Questions(json.load(f))


l_subjects = [{'label': i, 'value': i} for i in Q_ib2018.CD.get_subjects_taken()]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.Label('\nPlease choose between the following subjects:'),
    dcc.Dropdown(
        id='subject_dropdown',
        options=l_subjects
        #[
        #    {'label': 'New York City', 'value': 'NYC'},
        #    {'label': u'Montréal', 'value': 'MTL'},
        #    {'label': 'San Francisco', 'value': 'SF'}
        #],
    ),

    html.Label('\nWould you like to look at HL components (comparing only HL students)?'),

    dcc.RadioItems(
        id='yn_hl',
        options=[
            {'label': 'Yes', 'value': 'y'},
            {'label': 'No', 'value': 'n'},
        ],
        value='n'
    ),

    html.Label('\nPlease select 2 components to compare:'),

    dcc.Dropdown(
        id='components',
        options=[],
        multi=True
    ),

    html.Div(id='my_div'),

    dcc.Graph(
        id='q5',
        figure={
            'data': [
                go.Scatter(
                    x=[],
                    y=[],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name='name?'
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Component1'},
                yaxis={'title': 'Component2'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

# makes the subject components drop down
@app.callback(
    Output(component_id='components', component_property='options'),
    [Input(component_id='subject_dropdown', component_property='value'),
     Input(component_id='yn_hl', component_property='value')]
)
def update_dropdown(s_subject, s_hl):
    b_hl = True if s_hl == 'y' else False
    set_components = Q_ib2018.CD.get_subject_components(s_subject, b_hl)
    return [{'label': i, 'value': i} for i in set_components]

# makes the graph
@app.callback(
    Output(component_id='q5', component_property='figure'),
    [Input(component_id='subject_dropdown', component_property='value'),
     Input(component_id='yn_hl', component_property='value'),
     Input(component_id='components', component_property='value')
    ]
)
def update_graph(s_subject, s_hl, components):
    b_hl = True if s_hl == 'y' else False
    if components == None or len(components) != 2:
        return "Please choose 2 components from the above dropdown"

    l_comp1, l_comp2, slope, intercept, r_square = Q_ib2018.q5(s_subject, b_hl, *components)

    xmin, xmax = 0, max(l_comp1) + 10
    xs = np.linspace(0, xmax)
    ys = slope * xs + intercept

    return {
            'data': [
                go.Scatter(
                    x=l_comp1,
                    y=l_comp2,
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15#,
                        #'line': {'width': 0.5, 'color': 'white'}
                    },
                    name='Grade',
                    showlegend=False
                    # line={
                    #     'shape': 'linear'
                    # }
                ),
                go.Scatter(
                    x=xs,
                    y=ys,
                    mode='lines',
                    name=f"{round(slope, 1)}x + {round(intercept, 2)}, R$^2$={r_square:.3f}",
                    showlegend=True
                )
            ],
            'layout': go.Layout(
                xaxis={'title': components[0]},
                yaxis={'title': components[1], 'range': [0, max(l_comp2) + 10]},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }

if __name__ == '__main__':
    app.run_server(debug=True)