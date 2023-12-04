from pymongo import MongoClient
from config import *
import streamlit as st
import pandas as pd
import pymongo
import numpy as np
from config import * 
from bson.objectid import ObjectId

st.set_page_config(layout="wide",initial_sidebar_state ="collapsed")
st.title("Update")
client = MongoClient(MONGODB_CLUSTER, serverSelectionTimeoutMS=60000)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

revs = []
for rev in collection.find({"MovieName":"Parasite_2019"}).sort("helpful",pymongo.DESCENDING).limit(11):
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
    for select_id in selected_ids:
        select_id = ObjectId(select_id)
        update_criteria = {
            "_id": select_id}
        update_action = {
            "$inc": {
                "helpful": 1,
                "total_votes": 1
            }
        }
        collection.update_one(update_criteria, update_action)
    

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button("Submit Update",help="It will submit the reviews that you selected to the database",on_click=click_button)

if st.session_state.clicked:
    update_database(selected_ids)
    st.write("Updated the database, refresh to see the results")
