from bs4 import BeautifulSoup
import pandas as pd
import requests,re
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
    main_table = None
    main_section = soup.find('body')
    tmp = main_section.findAll('div',recursive=False)
    for i,div in enumerate(tmp):
        table = div.find('table',{'class':'tableBorder'},recursive=False)
        if not table:
            continue
        if table.find('tr',{'class':'tableLedger'}):
            print('found main table')
            main_table = table.parent
    """
    if not main_table:
    main_section = soup.find('body')
    tmp = main_section.findAll('div',recursive=False)
    
    for i,div in enumerate(tmp):
        table = div.find('table',{'class':'tableBorder'},recursive=False)
        if not table:
            continue
        if table.find('tr',{'class':'tableLedger'}):
            print('found main table')
    parent = table.parent
    #print(table.text)
    """
    ## Identify the total number of pages in thread
    pages_counter = main_table.findAll('a',{"class":"pageLink"})

    pages = 1
    if pages_counter:
        all_pages = [cur_page.text for cur_page in pages_counter]
        pages = int(all_pages[-2])

    ## Scrape all pages
    print("total num of pages = {}".format(pages))

    pattern = """([a-zA-Z\/_\-\.:0-9]+).html"""
    p = re.compile(pattern)
    base_link = re.search(p,url).group(1)

    for page_num in range(1,pages+1):
        print("scraping page {}".format(page_num))
        if page_num ==1:
            df = scrape_page(url,page_num,local=False)
            all_df = df
        else:
            df = scrape_page(base_link,page_num,local=False)
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
        page_url = "{base}_page{num}.html".format(base=url,num=page)
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
    main_table = None
    main_section = soup.find('body')
    tmp = main_section.findAll('div',recursive=False)
    for i,div in enumerate(tmp):
        table = div.find('table',{'class':'tableBorder'},recursive=False)
        if not table:
            continue
        if table.find('tr',{'class':'tableLedger'}):
            print('found main table')
            main_table = table
    if not main_table:
        raise ValueError("no main table identified")
    #print(main_table.text)

    comments = main_table.find('tr',{'class':None})
    #print("number of tr tags with no class :{}".format(len(comments)))
    details = main_table.select('tr.msgOddTableRow, tr.msgEvenTableRow')
    #print("number of tr tags with odd/even class:{}".format(len(details)))
    
    authors = main_table.select('td.msgEvenTableSide,td.msgOddTableSide')

    for detail in details:
        post_comment = detail.find('div',{'class':'msgBody'})
        if not post_comment:
            continue
        for tag in post_comment.find_all(['td']):
            tag.replace_with('')
        all_message_text.append(post_comment.text)
        #print(post_comment.text)
        #print("-------------------------------")#try:
    for author in authors:
        post_id = author.find('a')
        if not post_id:
            continue
        post_id_text = post_id['name']
        #print(post_id_text)
        user_name = author.find('span',{"class":"msgSideProfile"}).text
        #print(user_name)
        post_date_section = None
        post_date = author.parent.find('td',{'class':'msgOddTableTop'})
        post_date2 = author.parent.find('td',{'class':'msgEvenTableTop'})
        if post_date:
            post_date_section = post_date
        elif post_date2:
            post_date_section = post_date2
        else:
            print("no post_date available")
        if post_date_section:
            for tag in post_date_section.find_all(['span']):
                tag.replace_with('')
            post_date_ = post_date_section.text
        all_msg_id.append(post_id_text)
        all_user_name.append(user_name)
        all_reply_msg_id.append(None)
        all_post_date.append(post_date_)

    
    print(len(all_msg_id),len(all_message_text),len(all_user_name),
    len(all_reply_msg_id),len(all_post_date))

    final_df = pd.DataFrame({'message_id':all_msg_id,
        'clean_text':all_message_text,
        'user_name':all_user_name,
        'reply_msg_id':all_reply_msg_id,
        'post_date':all_post_date}
        )

    print(final_df.shape)
    return final_df
    

if __name__=="__main__":
    #url = '../../rawData/test-MyTableTennisNetThread1.html'
    #scrape_page(url,page=1,local=True)
    #scrape_thread(url,local=True)
    #url = 'https://www.tabletennisdaily.com/forum/showthread.php?10953-Tenergy-25-compared-to-Tenergy-05'
    url = 'http://mytabletennis.net/forum/h3-neo-what-degree-hardness-do-you-prefer_topic50552.html'
    #scrape_page(url,page=1,local=False)
    #url="https://ooakforum.com/viewtopic.php?f=44&t=24689"
    scrape_thread(url,local=False)

 
        
