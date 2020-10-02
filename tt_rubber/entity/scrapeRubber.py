from bs4 import BeautifulSoup
import pandas as pd
import requests

def scrape_thread(url,local=True):
    if local:
        print("reading local file!")
        with open(url) as fp: 
            soup = BeautifulSoup(fp,features="html.parser")
    ## Retrieve Rubber Brand
    brands = soup.findAll('div',{'class':'dbcat max-xxs no-radius-xxs no-side-border-xxs'})
    print(len(brands))
    
    all_brand_names = [ brand.find('a').text.strip() for brand in brands ]
    rubber_list = soup.findAll('table',{'class':'specscompare no-side-border-xxs'})
    print(len(rubber_list))
    for i,table in enumerate(rubber_list):
        cur_brand = all_brand_names[i]
        df = scrape_table(table,cur_brand)
        if i ==0:
            all_df = df
        else:
            all_df = pd.concat([all_df,df],axis=0)
            print(all_df.shape)
    return all_df
    
def scrape_table(table,rubber_brand):

    all_name = []
    all_speed = []
    all_spin = []
    all_tackiness = []
    all_overall = []
    all_price = []
    all_ratings = []

    all_rows = table.findAll('tr',{'class':None})
    print(len(all_rows))

    all_row_info = []
    for row in all_rows:
        all_cols = row.findAll('td',recursive=False)
        row_info = [col.text.strip() for col in all_cols]
        all_row_info.append(row_info)
        #print(row_info)
    
    df = pd.DataFrame(all_row_info)
    df.columns = ['name','speed','spin','tackiness','overall','price','ratings']
    #df.loc[:,'brand'] = rubber_brand
    df = df.assign(brand=[rubber_brand]*len(df))
    print(df.shape)
    return df

if __name__=="__main__":
    file_name = '../../rawData/revSpin_rubberList.html'
    output_df = scrape_thread(file_name)
    print(output_df.shape)

    output_df.to_csv('../output/revspin_rubber_list.csv',index=False)
    print("export completed")



