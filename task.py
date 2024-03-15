from newsapi import NewsApiClient
import requests
import pandas as pd
import pymysql.cursors
import random
from datetime import datetime
import json
from openai import OpenAI

def get_news_headlines(domains='cnn.com, foxnews.com, dailymail.co.uk, theguardian.com, reuters.com, finance.yahoo.com, forbes.com, bbc.co.uk, bbc.com, nytimes.com, news.google.com', 
                      language='en', 
                      from_param='2024-03-03T00:00:00', 
                      to_param='2024-03-04T00:00:00', 
                      sort_by='popularity',
                      page_size=100,
                      api_key='c30415236c3e4c7ea2b547eeb757e0c6'):
    api_query = f'https://newsapi.org/v2/everything?domains={domains}&language={language}&from={from_param}&to={to_param}&sortBy={sort_by}&pageSize={page_size}&apiKey={api_key}'

    response = requests.get(api_query)
    
    if response.status_code == 200:
        data_return = response.json()
        #reverse from least popular to most popular among the {page_size} articles
        data_return['articles'] = list(reversed(data_return['articles']))

        total_results = data_return.get('totalResults', 0)
        #print(f"Total results: {total_results}")
        
        # Select four random articles
        random_articles = random.sample(data_return['articles'], 4)
        #print(random_articles)

        return random_articles
    
def update_csv():
    
    check_data_return = get_news_headlines()

    database = pd.DataFrame(columns=['group_id', 'title', 'published_at', 'url_to_image', 'keywords'])
    for i in range(4):
        database.loc[len(database.index)] = [i+1,
                                            check_data_return[i]["title"],
                                            check_data_return[i]["publishedAt"],
                                            check_data_return[i]["urlToImage"],
                                            ["null","null","null","null"]]
    database.to_csv("database.csv")

if __name__=="main":
    update_csv()