# ds4a-t15-tableTennis-product-review
Comparative Table Tennis product review

## Folder Structure:
- |-- EDA: Folders contain data analysis jupyter notebook
- |-- labeling: create labelled data as well as training/testing/eval set
- |-- lexicon: extracting comparative lexicon
- |-- output: directory for output files after processing
- |-- tt_rubber: main modules for deployment
-    |-- common: connect to db
-    |-- entity: entity mapping
-    |-- scraper: webscraping moduel
-    |-- viz: Wordcloud visualization

## Create Local Testing Environment
- `conda create -n ds4a-t15 python=3.7 pip`
- `conda activate ds4a-t15`
- `pip install -r requirements.txt`

