import pandas as pd
import json

direction_dict= dict()
direction_dict[0]='g'
direction_dict[1]='e'
direction_dict[2]='l'

def subset_data(hoverData,json_cleaned_data):
    tmp = json.loads(hoverData)
    aspect = tmp['points'][0]['label'].split(' [')[0]
    entity_idx = tmp['points'][0]['curveNumber']

    df = pd.read_json(json_cleaned_data)
    filter_1 = df['ASPECT']==aspect
    filter_2 = df['DIRECTION']== direction_dict[entity_idx]
    
    short_df = df.loc[(filter_1)&(filter_2)]
        
    return short_df


