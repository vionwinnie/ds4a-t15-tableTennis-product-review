import pandas as pd
import sqlite3

def connect_to_db(local=True):
    """ 
    initialize connection to local sqlite3
    """
    con = None
    if local:
        # Create a SQL connection to our SQLite database
        con = sqlite3.connect("./db/tableTennisData.db")
    
    return con 

def retrieve_data(query):
    con = connect_to_db()
    df = pd.read_sql_query(query, con)
    con.close()
    return df

def retrieve_two_rubbers_stats(entity1,entity2,transpose=True):
    query = """select * from rubbers where name in ('{}','{}')""".format(entity1,entity2)
    df = retrieve_data(query)
    if transpose:
        df = df.transpose()
    df.reset_index(inplace=True)
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    return df

def retrieve_comparative_comments(entity1,entity2):

    """ 
    Retrieve comparative rubber statement from db
    """

    ## 
    if entity1 < entity2:
        rubber_a = entity1
        rubber_b = entity2
    else:
        rubber_a = entity2
        rubber_b = entity1

    query = """select * from comments where entity1='{}' and entity2='{}' """.format(rubber_a,rubber_b)

    df = retrieve_data(query)
    return df 


if __name__=="__main__":
    entity1 = 'Hurricane 3'
    entity2 = 'Tenergy 05'
    df = retrieve_comparative_comments(entity1,entity2)

    if len(df) > 0:
        for row in df.iterrows():
            print(row[1])
