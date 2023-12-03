import pandas as pd
import os
from pymongo import MongoClient
from datetime import datetime
from config import *


def convert_to_date(date_str: str):
    date_format = "%d %B %Y"
    converted_date = datetime.strptime(date_str, date_format)
    return converted_date


def insert_format(
    movie_name: str,
    review_folder: str = SAVE_FOLDER,
    wikipedia_folder: str = "wikipedia_data",
):
    csv_name = movie_name + ".csv"
    txt_name = movie_name + ".txt"
    movie_df = pd.read_csv(os.path.join(review_folder, csv_name))
    fill_values = {
        "review_date": "",
        "review_title": "",
        "review_comment": "",
        "review_rating": -1,
        "review_link": "",
        "reviews_if_spoiler": False,
        "review_total_votes": 0.0,
        "review_helpful": 0.0,
    }
    movie_df.fillna(fill_values, inplace=True)
    with open(os.path.join(wikipedia_folder, txt_name), "r") as f:
        wiki_data = f.read()
    movie_list = []
    for _, row in movie_df.iterrows():
        movie_dict = {}
        movie_dict.update({"MovieName": movie_name})
        movie_dict.update(
            {
                    "date": convert_to_date(row["review_date"]),
                    "title": row["review_title"],
                    "comment": row["review_comment"],
                    "rating": int(row["review_rating"]),
                    "link": row["review_link"],
                    "helpful": row["review_helpful"],
                    "total_votes": row["review_total_votes"],
                    "if_spoiler": row["reviews_if_spoiler"],
                    "source": "imdb"
            }
        )
        movie_list.append(movie_dict)
    movie_list.append({"MovieName": movie_name, "source": "wikipedia"})

    return movie_list


def connect_mongo(
    mongo_uri: str,
    database_name: str = DATABASE_NAME,
    collection_name: str = COLLECTION_NAME,
):
    client = MongoClient(mongo_uri)
    movie_database = client.get_database(name=database_name)
    movie_collection = movie_database[collection_name]
    return movie_collection


def main_insert(
    reviews_folder: str = SAVE_FOLDER, wikipedia_folder: str = WIKIPEDIA_FOLDER
):
    movie_collection = connect_mongo(MONGODB_CLUSTER)
    insert_many_list = []
    for movie in os.listdir(reviews_folder):
        if ".csv" in movie:
            movie_name = movie.split(".")[0]
            movie_dict = insert_format(
                movie_name,
                review_folder=reviews_folder,
                wikipedia_folder=wikipedia_folder,
            )
            insert_many_list.extend(movie_dict)
    movie_collection.insert_many(insert_many_list)


if __name__ == "__main__":
    main_insert()
