from bs4 import BeautifulSoup
import pandas as pd
import requests

def scrape_thread(url,local=True):
    if local:
        print("reading local file!")
        with open(url) as fp:
            soup = BeautifulSoup(fp,features="html.parser")
    else:
        page = requests.get(url)
#        print(page.status_code)
        if page.status_code==200:
            soup = BeautifulSoup(page.text,features="html.parser")
        else:
            raise ValueError("requests unable to fetch the page") 
     ## Identify the div that contains thread
     ##threads = soup.find('div', id='threadlist')

    ## Identify the total number of pages in thread
    pages_counter = soup.find('td',{"class":"nav"})

    pages = 1 #default as only 1 page
    if pages_counter:
        pages_text = pages_counter.text
        pages = int(pages_text.split("of ")[1])

    ## Scrape all pages
    print("total num of pages = {}".format(pages))

    for page_num in range(1,pages+1):
        print("scraping page {}".format(page_num))
        df = scrape_page(url,page_num,local=False)
        if page_num ==1:
            all_df = df
        else:
            all_df = pd.concat([all_df,df],axis=0)
        print(all_df.shape)

    all_df.drop_duplicates(inplace=True)
    print(all_df.shape)
    return all_df
    

def scrape_page(url,page,local=True):
    ## text string for specific page
    if page ==1:
        page_url = url
    else:
        comment_num = (page-1)*15
        page_url = "{base}&start={num}".format(base=url,num=comment_num)
    print(page_url)

    ## parsing html
    if local:
        print("reading local file!")
        with open(page_url) as fp: 
            soup = BeautifulSoup(fp,features="html.parser")
    else:
        page = requests.get(page_url)
        if page.status_code==200:
            soup = BeautifulSoup(page.text,features="html.parser")
        else:
            raise ValueError("requests unable to fetch the page") 
   # print("length of soup:{}".format(len(soup.text)))
    
    all_msg_id = []
    all_message_text = []
    all_user_name = []
    all_reply_msg_id = []
    all_post_date = []
    
    ## each post
    comments = soup.findAll('table',{"class":"tablebg"})
    print('found {} rows'.format(len(comments)))

    ## extract the table with 
    for comment in comments:
        details = comment.select('tr.row1, tr.row2')

        if not details:
            continue

        ## divided into first and second tr
        user_row = details[0]
        comment_row = details[1]

        ## extract user_name, msg_id, post_date
        user_name = user_row.find('b',{"class":"postauthor"}).text
        msg_id = user_row.find('a')['name']
        reply_msg_id = None

            
        post_details = user_row.find('td',{"class":"gensmall"})
        post_date = post_details.find('div',{"style":"float: right;"}).text
        final_date = post_date.replace('Posted:','')
            
        ## extract comment
        comment = comment_row.findAll('table')[1].findAll('div',{"class":"postbody"})[0]
        for tag in comment.find_all(['div']):
            tag.replace_with('')

        comment_text = comment.text
        print("----------------------------------------------------")
        print(user_name,msg_id,reply_msg_id,final_date,comment_text)

        all_msg_id.append(msg_id)
        all_message_text.append(comment_text)
        all_user_name.append(user_name)
        all_reply_msg_id.append(reply_msg_id)
        all_post_date.append(final_date)

    final_df = pd.DataFrame({'message_id':all_msg_id,
        'clean_text':all_message_text,
        'user_name':all_user_name,
        'reply_msg_id':all_reply_msg_id,
        'post_date':all_post_date}
        )

    print(final_df.shape)
    return final_df


if __name__=="__main__":
    #url = '../../rawData/test-Oak2.html'
    #scrape_page(url,page=1,local=True)
    #scrape_thread(url,local=True)
    #url = 'https://www.tabletennisdaily.com/forum/showthread.php?10953-Tenergy-25-compared-to-Tenergy-05'
    #scrape_page(url,page=1,local=False)
    url="https://ooakforum.com/viewtopic.php?f=44&t=24689"
    scrape_thread(url,local=False)

 
