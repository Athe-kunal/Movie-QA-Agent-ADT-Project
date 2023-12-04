import streamlit as st
from pymongo import MongoClient
import os
from config import *
# MongoDB setup
# conn_str = "mongodb+srv://imdb_adt:imdb_adt@cluster0.rcvxgzc.mongodb.net/"
client = MongoClient(MONGODB_CLUSTER, serverSelectionTimeoutMS=60000)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Streamlit UI
st.title("Movie Review Manager")

# Input for movie name
movie_name = st.text_input("Enter the movie name:", "Parasite_2019")

# Button to delete reviews
if st.button('Delete Required Reviews'):
    try:
        # MongoDB operation to delete reviews
        # Reviews with 'helpful' equal to 0 and 20 words or fewer in 'text'
        delete_criteria = {
            "MovieName": movie_name.strip(), 
            "helpful": 0,
            "comment": {"$regex": r"^\b(\w+\b\W*){0,20}$"}
        }
        result = collection.delete_many(delete_criteria)
        
        # Display the result
        st.write(f"Documents deleted: {result.deleted_count}")
    except Exception as e:
        st.write("An error occurred:", e)
