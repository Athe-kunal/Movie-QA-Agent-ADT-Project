from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd
from langchain.schema import Document
from config import *
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.embeddings import SentenceTransformerEmbeddings
from pymongo import MongoClient
from datetime import datetime
import os


def convert_to_date(date_str: str):
    date_format = "%d %B %Y"
    converted_date = datetime.strptime(date_str, date_format)
    return converted_date


def get_docs(movie_name: str, if_split: bool = True):
    df = pd.read_csv(f"{SAVE_FOLDER}\{movie_name}.csv")
    docs = []
    for i in df.iterrows():
        row = i[1]
        docs.append(
            Document(
                page_content=row["review_title"] + " " + row["review_comment"],
                metadata={
                    "date": convert_to_date(row["review_date"]),
                    "title": row["review_title"],
                    "rating": row["review_rating"],
                    "helpful": row["review_helpful"],
                    "total_votes": row["review_total_votes"],
                    "if_spoiler": row["reviews_if_spoiler"],
                    "link": row["review_link"],
                    "MovieName": movie_name,
                    "source": "imdb",
                },
            )
        )

    with open(f"{WIKIPEDIA_FOLDER}\{movie_name}.txt", "r") as f:
        data = f.read()
        docs.append(
            Document(
                page_content=data,
                metadata={"MovieName": movie_name, "source": "wikipedia"},
            )
        )
    if if_split:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=32)
        docs = text_splitter.split_documents(docs)
    return docs


def insert_vectordb(docs):
    # initialize MongoDB python client
    client = MongoClient(MONGODB_CLUSTER)
    MONGODB_COLLECTION = client[DATABASE_NAME][VECTORDB_COLLECTION_NAME]
    vector_search = MongoDBAtlasVectorSearch.from_documents(
        documents=docs,
        embedding=SentenceTransformerEmbeddings(model_kwargs={"device": "cuda"}),
        collection=MONGODB_COLLECTION,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )


def insert_main():
    for movie_name in os.listdir(SAVE_FOLDER):
        movie_name = movie_name.split(".")[0]
        docs = get_docs(movie_name)
        insert_vectordb(docs)
        print(f"Done for {movie_name}")


if __name__ == "__main__":
    insert_main()
