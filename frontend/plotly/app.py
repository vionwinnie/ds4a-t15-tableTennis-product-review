import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc 
import pandas as pd
import createBarChart as cbc

external_stylesheets = [dbc.themes.BOOTSTRAP,'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, 
        external_stylesheets=external_stylesheets,
        title='Rubber Shopper!')

dropdown_menu1=dcc.Dropdown(
        id='demo-dropdown1',
        options=[
            {'label': 'Butterfly Tenergy 05', 'value': 'Tenergy 05'},
            {'label': 'Hurricane 3', 'value': 'Hurricane 3'},
            {'label': 'Evolution MX-P', 'value': 'MXP'}
        ],
        value='',
        style={'float': 'center','margin': 'auto'},
        placeholder="Select Rubber A"
        )
dropdown_menu2=dcc.Dropdown(
        id='demo-dropdown2',
        options=[
            {'label': 'Butterfly Tenergy 05', 'value': 'Tenergy 05'},
            {'label': 'Hurricane 3', 'value': 'Hurricane 3'},
            {'label': 'Evolution MX-P', 'value': 'MXP'}
        ],
        value='',
        style={'float': 'center','margin': 'auto'},
        placeholder="Select Rubber B"
        )

df = pd.DataFrame(
    {
        "First Name": ["Arthur", "Ford", "Zaphod", "Trillian"],
        "Last Name": ["Dent", "Prefect", "Beeblebrox", "Astra"],
    }
)

table = dbc.Table.from_dataframe(df, striped=True, 
                                     bordered=True, 
                                     hover=True,
                                     dark=True,
                                     responsive=True,
                                     className='dataTable')

app.layout = html.Div([
    ## Row with columns
    dbc.Row(
    [
                dbc.Col(dropdown_menu1,width=3),
                dbc.Col(dropdown_menu2,width=3),
    ]),
    dbc.Row([dbc.Col(html.Div(id='dd-entity-container'))]),
    dbc.Row([dbc.Col(dcc.Graph(style={'height':300},id='comparison-graph'))]),
    dbc.Row([dbc.Col(html.Div(id='table-container'),width={"size": 3, "order": "last", "offset": 1},)]),
    dbc.Row([
        dbc.Col(html.Img(id='wordcloud-entity1',className='wordcloud'),width=3),
        dbc.Col(html.Img(id='wordcloud-entity2',className='wordcloud'),width=3)
        ],justify="start")
    ]
    ,className="dash-bootstrap")

## update graph from dropdown menu
@app.callback(
    Output('comparison-graph', 'figure'),
    [Input('demo-dropdown1', 'value'),
    Input('demo-dropdown2', 'value')
    ])
def update_graph(value1,value2):
    print(value1,value2)

    if len(value1)==0 or len(value2)==0: 
        return {'data':[], 'layout':go.Layout()}
    else:
        df = cbc.create_dummy_df()
        fig = cbc.create_chart(df,value1,value2)
        return fig
    #return 'Entity 1: "{}"'.format(value)

## update textbox from dropdown menu
@app.callback(
    Output('dd-entity-container', 'children'),
    [Input('demo-dropdown1', 'value'),
    Input('demo-dropdown2', 'value')])
def update_output(value1,value2):
    if len(value1)==0 or len(value2)==0:
        return "Please select two rubbers!"
    elif value1 == value2:
        return "You have selected the same rubber twice. Try again"
    else:
        return 'You are now comparing {} against {}!'.format(value1,value2)

@app.callback(
    Output('table-container', 'children'),
    [Input('demo-dropdown1', 'value'),
    Input('demo-dropdown2', 'value')])
def update_output(value1,value2):
    if len(value1)==0 or len(value2)==0:
        return None#"Please select two rubbers!"
    elif value1 == value2:
        return None #"You have selected the same rubber twice. Try again"
    else:
        return table


## update wordcloud from dropdown menu
static_image_route = '/assets/'
@app.callback(
    dash.dependencies.Output('wordcloud-entity1', 'src'),
    [dash.dependencies.Input('demo-dropdown1', 'value')])
def update_image_src(value):
    if not value:
        return None
    else:
        new_val = value.replace(' ','-')
        path = static_image_route + new_val + '.png'
        return path


@app.callback(
    dash.dependencies.Output('wordcloud-entity2', 'src'),
    [dash.dependencies.Input('demo-dropdown2', 'value')])
def update_image_src(value):
    if not value:
        return None
    else:
        new_val = value.replace(' ','-')
        path = static_image_route + new_val + '.png'
        return path


if __name__ == '__main__':
    app.run_server(debug=True)
