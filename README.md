## ds4a-t15-tableTennis-product-review
- Contributor: Charlotte Giang, Eyan Yeung, Pooja Umathe, Jessie Zhang,Winnie Yeung (Team Lead)
- Our team implements natural language processing models to mine comparative opinions on table tennis products
- Tech Stack: MongoDB, Sqlite3, Python, Flask, Dash, Plotly, Fastapi, CSS, Bootstrap, Heroku
- Live Deployment: http://tabletennis-equipment-showdown.herokuapp.com/

## Directory Structure:
- |-- EDA: Folders contain data analysis jupyter notebook
- |-- scraper: webscraping/data ETL module
- |-- comparison: Roberta classification model training using labelled data and inferencing on unlabelled data
- |-- information_retrieval: Extracting Entity, Attribute, Directions from comparative sentences 
- |-- common: common utils (connect to db, data query)
- |-- viz: wordcloud visualization
- |-- frontend: dashboard 

## Create Local Testing Environment
- `conda create -n ds4a-t15 python=3.7 pip`
- `conda activate ds4a-t15`
- `pip install -r requirements.txt`

## Fire up Local Front End Environment
- `cd frontend`
- `python app.py`
- Open up Google Chrome Browse to http://127.0.0.1:8888

## Fire up local sqlite db
- `cd frontend/db`
- `sqlite3`
- `sqlite> .open tableTennisData.db`

## Further Reading
- Slide Deck Presentation for DS4A conference (10/16/2020): https://bit.ly/35eXcqD
