import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc 
import pandas as pd
import createBarChart as cbc
import connectDb as c
import nameConversion

## Initialize app with CSS stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP,'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, 
        external_stylesheets=external_stylesheets,
        title='Rubber Shopper!')

## Intialize Sqlite3 db connection
con = c.connect_to_db()


## Define Dropdown Menu Components
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

## define name lookup for revspin data
revSpinDict = nameConversion.revSpinDict
#print(revSpinDict)



app.layout = html.Div([
    html.H1('Your Go-To Table Tennis Rubber Analyzer',
        style={'text-align':'center','margin-top':'30px'}),
    ## Row with columns
    dbc.Row(
    [
                dbc.Col(dropdown_menu1,
                    width={"size": 3, "order": "first", "offset":3 }),
                dbc.Col(dropdown_menu2,
                    width={"size": 3, "order": "first",  })
    ]),
    dbc.Row([dbc.Col(html.Div(id='dd-entity-container'))],style={"margin-top": "15px","text-align":"center"}),
    dbc.Row([dbc.Col(dcc.Graph(style={'height':300},id='comparison-graph'),
        width={"size": 5, "order": "first", "offset": 1})],
        style={"margin-top":"15px"},),
    dbc.Row([
        dbc.Col(
            html.Div([
            html.Div([
                    html.Div([
                            html.H4(id = "status",
                            className = "subtitle",
                            children=["init"])]),

                            dcc.Interval(id="update1",interval=1000)
                            ]),
            html.Div(id='table-container',
                    className='dataTable'),]),
            width={"size": 4, "order": "first", "offset": 1},),
        dbc.Col(
            html.Div([
            html.Div([
                    html.Div([
                            html.H4(id = "status-wordcloud1",
                            className = "subtitle",
                            children=["init"])]),

                            dcc.Interval(id="update2",interval=1000)
                            ]),
            html.Img(id='wordcloud-entity1',
            className='wordcloud'),]),
            width=3),
        dbc.Col(
            html.Div([
            html.Div([
                    html.Div([
                            html.H4(id = "status-wordcloud2",
                            className = "subtitle",
                            children=["init"])]),
                            dcc.Interval(id="update3",interval=1000)
                            ]),
            html.Img(id='wordcloud-entity2',
            className='wordcloud')]),
            width=3)],
        style={"margin-top":"80px"},
        justify='start'),
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
        if value1 < value2:
            rubber_a = value1
            rubber_b = value2
        else:
            rubber_a = value2
            rubber_b = value1
        df = c.retrieve_comparative_comments(rubber_a,rubber_b)
        tally_df = cbc.transform_df_barchart(rubber_a,rubber_b,df)
        if len(tally_df)==0:
            return {'data':[],'layout':go.Layout()}
        else:
            fig = cbc.create_chart(tally_df,rubber_a,rubber_b)
            return fig

## update textbox from dropdown menu
@app.callback(
    Output('dd-entity-container', 'children'),
    [Input('demo-dropdown1', 'value'),
    Input('demo-dropdown2', 'value')])
def update_output(value1,value2):
    if not value1  or not value2:
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
        rubber1 = revSpinDict.get(value1,None)
        rubber2 = revSpinDict.get(value2,None)
        print(rubber1,rubber2)
        df = c.retrieve_two_rubbers_stats(rubber1,rubber2,transpose=True)
        table = dbc.Table.from_dataframe(df, striped=True, 
                                     bordered=True, 
                                     hover=True,
                                     dark=True,
                                     responsive=True)
        return table


## update wordcloud1 from dropdown menu
static_image_route = '/assets/'
@app.callback(
    Output('wordcloud-entity1', 'src'),
    [Input('demo-dropdown1', 'value')])
def update_image_src(value):
    if not value:
        return None
    else:
        new_val = value.replace(' ','-')
        path = static_image_route + new_val + '.png'
        return path

## update wordcloud2 image
@app.callback(
    Output('wordcloud-entity2', 'src'),
    [Input('demo-dropdown2', 'value')])
def update_image_src(value):
    if not value:
        return None
    else:
        new_val = value.replace(' ','-')
        path = static_image_route + new_val + '.png'
        return path

## Display Table Name
@app.callback(Output("status", "children"),
              [Input('demo-dropdown1', 'value'),
               Input('demo-dropdown2', 'value')])
def update_statusBar(value1,value2):
    if value1 and value2:
        return "RevSpin Data"

## Display Wordcloud1 Title
@app.callback(Output("status-wordcloud1", "children"),
              [Input('demo-dropdown1', 'value'),
            ])
def update_statusBar(value1):
    if value1:
        return value1+" Wordcloud"

## Display Wordcloud2 Title
@app.callback(Output("status-wordcloud2", "children"),
              [Input('demo-dropdown2', 'value'),
            ])
def update_statusBar(value1):
    if value1:
        return value1+" Wordcloud"



if __name__ == '__main__':
    app.run_server(debug=True,port=8888)
