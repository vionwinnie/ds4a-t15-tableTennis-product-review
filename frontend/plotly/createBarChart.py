import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import connectDb as c

def create_chart(data,entity1,entity2):
    
    x_1 = "{} %".format(entity1)
    x_2 = "Equal %"
    x_3 = "{} %".format(entity2)
    title_text = "{} vs {} Aspect Comparison".format(entity1,entity2)
    
    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)')
    fig = go.Figure(layout=layout)

    fig.add_trace(go.Bar(
        x=data[x_1],
        y=data.ASPECT,
        name=x_1.replace('%',''),
        text=data[x_1].apply(lambda x: "{:.1f}{}".format(x, ' %')),
        textposition='inside',
        insidetextanchor = 'middle',
        marker=dict(
            color='rgba(50,50,50, 0.6)',
            line=dict(color='rgba(50,50,50, 0.8)', width=0.05)
        ),
        orientation='h'
    ))
    fig.add_trace(go.Bar(
        x=data[x_2],
        y=data.ASPECT,
        name=x_2.replace('%',''),
        text=data[x_2].apply(lambda x: "{:.1f}{}".format(x, ' %')),
        textposition='inside',
        insidetextanchor = 'middle',
        marker=dict(
            color='rgba(255,255,158, 0.6)',
            line=dict(color='rgba(225,255,224, 0.8)', width=0.05)
        ),
        orientation='h'

    ))
    fig.add_trace(go.Bar(
        x=data[x_3],
        y=data.ASPECT,
        name=x_3.replace('%',''),
        text=data[x_3].apply(lambda x: "{:.1f}{}".format(x, ' %')),
        textposition='inside',
        insidetextanchor = 'middle',
        marker=dict(
            color='rgba(128,0,0, 0.5)',
            line=dict(color='rgba(128,0,0, 0.8)', width=0.05)
        ),
        orientation='h'

    ))
    fig.update_layout(
            xaxis=dict(
            title_text="Discussion %",
            ticktext=["0%", "20%", "40%", "60%","80%","100%"],
            tickvals=[0, 20, 40, 60, 80, 100],
            tickmode="array",
            titlefont=dict(size=15),
        ),
        autosize=False,
        width=700,
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
#        title={
#            'text': title_text,
#            'y':0.96,
#            'x':0.5,
#            'xanchor': 'center',
#            'yanchor': 'top'},
        barmode='stack')
    return fig 

def create_dummy_df():
    df2 = pd.DataFrame({
        'aspect':['Control','Overall'],
        'Hurricane 3 %':[50,70],
        'Equal %':[10,20],
        'Tenergy 05 %':[40,10]
    })
    return df2

def transform_df_barchart(entity1,entity2,df):
   
    ## Count each subgroup
    tallying = df.groupby(['ASPECT','DIRECTION'])['COMMENT_ID'].count().reset_index()
    ## Calculate percentage
    tallying['SUBGROUP_PCT'] = tallying.COMMENT_ID / tallying.groupby('ASPECT')['COMMENT_ID'].transform('sum') *100
    ## Summarize percentage
    tallying_pivot_df = tallying.pivot(index='ASPECT', columns='DIRECTION', values='SUBGROUP_PCT')
    tallying_pivot_df.fillna(0,inplace=True)

    ## Rename using mapping
    col_conversion = dict(e='Equal %',g='{} %'.format(entity1),l='{} %'.format(entity2))
    tallying_pivot_df.rename(columns=col_conversion,inplace=True)
    tallying_pivot_df.reset_index(inplace=True)

    return tallying_pivot_df



if __name__=="__main__":
    df2 = pd.DataFrame({
        'ASPECT':['Control','Overall'],
        'Hurricane 3 %':[50,70],
        'Equal %':[10,20],
        'Tenergy 05 %':[40,10]
    })

    data = df2.copy()
    entity1='Tenergy 05'
    entity2='Hurricane 3'
    sample_fig = create_chart(df,entity1,entity2)
    #sample_fig.show()
