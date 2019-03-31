import os
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from questions import Questions


s_path = os.path.dirname(__name__)
s_path_data = os.path.join(s_path, "data")

s_cached_data_fname = os.path.join(s_path_data, 'cached_data.json')

with open(s_cached_data_fname) as f:
    Q_ib2018 = Questions(json.load(f))

l_compare = Q_ib2018.q6()

app = dash.Dash(__name__)  # , external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Graph(
        id='q6',
        figure={
            'data': [
                go.Scatter(
                    x=[i[0] for i in l_compare[subj]],  # TODO replace with dataframe ?
                    y=[i[1] for i in l_compare[subj]],
                    # text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=subj
                ) for subj in l_compare
            ],
            'layout': go.Layout(
                xaxis={'title': 'EE Grade'},
                yaxis={'title': 'Subject Grade'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
