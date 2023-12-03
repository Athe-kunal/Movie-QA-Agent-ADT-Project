from pymongo import MongoClient
from config import *
import streamlit as st
import pandas as pd
import pymongo
import numpy as np

st.set_page_config(layout="wide")
st.title("Update")
client = MongoClient(MONGODB_CLUSTER)
movie_database = client.get_database(name=DATABASE_NAME)
movie_collection = movie_database[COLLECTION_NAME]

revs = []
for rev in movie_collection.find({"MovieName":"Parasite_2019"}).sort("helpful",pymongo.DESCENDING).limit(11):
    if rev['source']=="imdb":
        revs.append(rev)
df = pd.DataFrame(revs)

ids = df['_id'].tolist()
helpful = df['helpful'].tolist()
total_votes = df['total_votes'].tolist()
helpful_votes = [str(int(helpful[i])) + "/" + str(int(total_votes[i])) for i in range(len(df))]
df['helpful/votes'] = helpful_votes
# df['found helpful'] = [False for _ in range(len(df))]
df.drop(['_id','MovieName','date','title','link','if_spoiler','source','helpful','total_votes'],inplace=True,axis=1)

# st.dataframe(df,use_container_width=True,hide_index=True)
def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(3, "found helpful?", False)
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"found helpful?": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
        use_container_width=True
    )
    selected_indices = list(np.where(edited_df['found helpful?'])[0])
    return selected_indices


selection = dataframe_with_selections(df)
selected_ids = [ids[select_id] for select_id in selection]

def update_database(selected_ids):
    movie_collection.update_many
    for select_id in selected_ids:
        movie_collection.update_many({'_id': select_id}, [{'$inc': {'helpful': 1}},{'$inc': {'total_votes': 1}}])
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button("Submit Update",help="It will submit the reviews that you selected to the database",on_click=click_button)

if st.session_state.clicked:
    update_database(selected_ids)
    st.write("Updated the database")



        
