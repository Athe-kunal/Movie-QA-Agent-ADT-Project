import pandas as pd
import os
from pymongo import MongoClient

def insert_format(movie_name:str,review_folder:str="movie_reviews_link",wikipedia_folder:str="wikipedia_data"):
    movie_dict = {}
    csv_name = movie_name+".csv"
    txt_name = movie_name+".txt"
    movie_df = pd.read_csv(os.path.join(review_folder,csv_name))
    fill_values = {'review_date':'', 'review_title':'', 'review_comment':'','review_rating':-1,'review_link':''}
    movie_df.fillna(fill_values,inplace=True)
    with open(os.path.join(wikipedia_folder,txt_name), 'r') as f:
        wiki_data = f.read()
    movie_dict.update({"MovieName":movie_name})
    movie_dict.update({"reviews":[]})
    for _,row in movie_df.iterrows():
        movie_dict['reviews'].append({
            "date":row['review_date'],
            "title":row['review_title'],
            "review":row['review_comment'],
            "rating":row['review_rating'],
            "link":row['review_link']}
        )
    movie_dict.update({"wikipedia":{"plot":wiki_data}})
    return movie_dict

def connect_mongo(mongo_uri:str,database_name:str="Moviedatabase",collection_name:str="Moviedatabase"):
    client = MongoClient(mongo_uri)
    movie_database = client.get_database(name=database_name)
    movie_collection = movie_database[collection_name]
    return movie_collection


