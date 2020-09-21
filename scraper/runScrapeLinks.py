import scrapeLinks
import pandas as pd

base_path = 'https://www.tabletennisdaily.com/forum/forumdisplay.php?102-Rubbers'

for i in range(1,46):
    page_path = "{base_path}/page{num}".format(base_path=base_path,num=i)
    print(page_path)

    cur_links = scrapeLinks.scrape_links(page_path,local=False)
    print(cur_links.shape)

    if i ==1:
        all_links = cur_links
    else:
        all_links = pd.concat([all_links,cur_links],axis=0)

    print(all_links.shape)

all_links.drop_duplicates(inplace=True)
print(all_links.shape)
output_path = '../output/tabletennisdaily_rubber_threads.csv'
all_links.to_csv(output_path,index=False)
print('export is completed')
