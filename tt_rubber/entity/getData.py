import connectMongo
import re
import pandas as pd

## Example of how to fetch data from MongoDB

## current forum options are 'tableTennisDaily' and 'ooakForum'
forum_name = 'ooakForum'
conn = connectMongo.connect_mongo('forums',forum_name)
myquery = { "meta_idx": { "$gt": 870 } }
mydoc = conn.find(myquery)

def generate_df_from_result(result):
    """
    input: mongodb query result
    output: dataframe
    """
    ids = []
    titles = []
    replies = []

    for idx,val in enumerate(result):
        # add to the lists
        ids.append(val['_id'])
        titles.append(val['title'])
        replies_arr = []

        for reply in val['replies'][1:]: # don't want the original post asking the question so use [1:]
            text = reply['clean_text'].replace('\n','') # want to get rid of the \n\n
            replies_arr.append(text)
        replies.append(replies_arr)
    df = pd.DataFrame({'id':ids,'thread_title':titles,'reply':replies})
    #df = df.explode('reply') # explode() to go from item in arr to row
    return df


# find all thread title that contains AND or '&' symbol (ignore case)
regex_and = re.compile("( and )|(\&)", re.IGNORECASE)
regex_and_result = conn.find({"title":regex_and},{"title":1,"replies.clean_text":1})
and_df = generate_df_from_result(regex_and_result)
print(and_df.shape)

regex_vs = re.compile("vs", re.IGNORECASE)
vs_result = conn.find({"title":regex_vs},{"title":1,"replies.clean_text":1})
vs_df = generate_df_from_result(vs_result)
print(vs_df.shape)

