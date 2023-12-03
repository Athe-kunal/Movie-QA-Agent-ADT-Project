import streamlit as st
from pymongo import MongoClient
import pandas as pd
import certifi
from config import MONGODB_CLUSTER, DATABASE_NAME, COLLECTION_NAME

# Connect to MongoDB
client = MongoClient(MONGODB_CLUSTER, tlsCAFile=certifi.where())
db = client[DATABASE_NAME]
ratings_collection = db[COLLECTION_NAME]

# Get distinct movie names from the database
distinct_movie_names = ratings_collection.distinct("MovieName")

# Streamlit App
st.title("Movie Reviews Explorer")

# Get user input for filtering reviews
movie_name = st.selectbox("Select Movie Name:", distinct_movie_names, key="movie_input")
start_date = st.date_input("Select Start Date:")
rating_options = ratings_collection.distinct("rating")
selected_rating_range = st.slider("Select Rating Range:", min_value=min(rating_options), max_value=max(rating_options), value=(min(rating_options), max(rating_options)))

# Fetch maximum values for helpful votes and total votes based on the selected movie
helpful_max_value = round(ratings_collection.find({"MovieName": movie_name}).sort("helpful", -1).limit(1)[0]['helpful'])
total_votes_max_value = round(ratings_collection.find({"MovieName": movie_name}).sort("total_votes", -1).limit(1)[0]['total_votes'])

helpful_votes_range = st.slider("Select Helpful Votes Range:", min_value=0, max_value=helpful_max_value, value=(0, helpful_max_value))
total_votes_range = st.slider("Select Total Votes Range:", min_value=0, max_value=total_votes_max_value, value=(0, total_votes_max_value))
spoiler_options = ["", True, False]  # Updated spoiler options
selected_spoiler = st.selectbox("Select Spoiler:", spoiler_options)
source_options = ratings_collection.distinct("source")
selected_source = st.selectbox("Select Source:", [""] + source_options)

# Button to show results
if st.button("Show Results"):

    # Create a filter dictionary based on user input
    filter_dict = {"MovieName": movie_name}
    if start_date:
        filter_dict["date"] = {"$gte": pd.to_datetime(start_date)}
    if selected_rating_range:
        filter_dict["rating"] = {"$gte": selected_rating_range[0], "$lte": selected_rating_range[1]}
    if helpful_votes_range:
        filter_dict["helpful"] = {"$gte": helpful_votes_range[0], "$lte": helpful_votes_range[1]}
    if total_votes_range:
        filter_dict["total_votes"] = {"$gte": total_votes_range[0], "$lte": total_votes_range[1]}
    if selected_spoiler != "":
        filter_dict["if_spoiler"] = selected_spoiler
    if selected_source:
        filter_dict["source"] = selected_source

    # Query MongoDB for reviews
    reviews_data = list(ratings_collection.find(filter_dict).limit(10))

    if not reviews_data:
        st.warning("No reviews found based on the selected criteria.")
    else:
      
        # Create DataFrame from MongoDB data
        df = pd.DataFrame(reviews_data)

        # Display the table for the top 10 reviews based on 'helpful'
        st.title(f'Top 10 Reviews for {movie_name} based on Helpful Votes')
        top_helpful_df = df.sort_values(by='helpful', ascending=False).head(10)
        # Remove the '_id' column from the DataFrame
        top_helpful_df = top_helpful_df.drop(columns=['_id'])

        # Display the table
        st.write(top_helpful_df.style.set_properties(**{'text-align': 'left'}))

container = st.empty()

def reset_conversation():
    st.session_state.movie_name = None
    container.empty()

st.button('Reset Input', on_click=reset_conversation)
