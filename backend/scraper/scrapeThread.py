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
    pages_counter = soup.find('div',id='pagination_top')
    pages = 1 #default as only 1 page
    if pages_counter:
        pages_text = pages_counter.find('a',{'class':'popupctrl'})
        if pages_text:
        #pages_text = pages_counter.find('a',id='yui-gen14')
 #           print(pages_text)
            pages = int(pages_text.text.split("of ")[1])

    ## Scrape all pages
    print("total num of pages = {}".format(pages))

    for page_num in range(1,pages+1):
  #      print("scraping page {}".format(page_num))
        df = scrape_page(url,page_num,local=False)
        if page_num ==1:
            all_df = df
        else:
            all_df = pd.concat([all_df,df],axis=0)
        #print(all_df.shape)

    all_df.drop_duplicates(inplace=True)
    #print(all_df.shape)

    return all_df

def scrape_page(url,page,local=True):
    ## text string for specific page
    if page ==1:
        page_url = url
    else:
        page_url = "{base}/page{num}".format(base=url,num=page)
    #print(page_url)

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
    
    msg_df = grab_message(soup)
    meta_df = find_post_metainfo(soup)
    final_df = pd.merge(left=meta_df,right=msg_df,on='message_id',how='left')

    print(msg_df.shape)
    print(meta_df.shape)
    print(final_df.shape)
    return final_df
def grab_message(soup):
    all_msg_id = []
    all_msg = []

    messages = soup.find_all('div')
    counter = 0
    for cur_message in messages:
        msg_id = cur_message.get('id',999)
        if msg_id !=999:
            if 'post_message_' in msg_id:
                counter +=1
                clean_id=msg_id.split('_')[2]
                for tag in cur_message.find_all(['div']):
                    tag.replace_with('')
                clean_message = cur_message.text.encode('utf-16','surrogatepass').decode('utf-16')
                #print(clean_message)
                #print("===========================")

                all_msg_id.append(clean_id)
                all_msg.append(clean_message)
    df = pd.DataFrame({'message_id':all_msg_id,'clean_text':all_msg})
#    print(df.clean_text)
    #print(counter)
    return df


def find_post_metainfo(soup):

    all_message_id = []
    all_message_text = []
    all_user_name = []
    all_reply_msg_id = []
    all_post_date = []
    
    all_comments = soup.findAll('li',{'class':"postbitlegacy postbitim postcontainer old"})
    #print("number of comments:{}".format(len(all_comments)))
    for i,comment in enumerate(all_comments):
        post_date = comment.find('span',{'class':'postdate old'}).text.replace("Posted",'').strip()
        user_name_block = comment.find('div',{'class':'username_container'})
        if user_name_block.find('a'):
            user_name = user_name_block.find('a').text
        else:
            user_name = user_name_block.find('span',{'class':'username guest'}).text
        message_id = comment['id'].split('_')[1]
        check_reply = comment.find('div',{'class':'quote_container'})
        if check_reply:
            reply_url = check_reply.find('a')['href']
            reply_post_id = reply_url.split('#')[1].replace('post','')
            print("reply:{}".format(reply_post_id))
        all_message_id.append(message_id)
        #all_message_text.append(message)
        all_user_name.append(user_name)
        if check_reply:
            all_reply_msg_id.append(reply_post_id)
        else:
            all_reply_msg_id.append(None)
        all_post_date.append(post_date)

    df = pd.DataFrame({'message_id':all_message_id,
            'user_name':all_user_name,
            'reply_msg_id':all_reply_msg_id,
            'post_date':all_post_date}
            )
    print(df.shape)
    return df

if __name__=="__main__":
    #url = '../rawData/file.txt'
    #scrape_page(url,page=1,local=True)
    #url = 'https://www.tabletennisdaily.com/forum/showthread.php?10953-Tenergy-25-compared-to-Tenergy-05'
    #scrape_page(url,page=1,local=False)
    url = 'https://www.tabletennisdaily.com/forum/showthread.php?23999-Are-ZLC-blades-even-popular'
    scrape_thread(url,local=False)

    #scrape_page(url,page=1,local=False)
 
