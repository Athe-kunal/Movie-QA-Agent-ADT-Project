import streamlit as st
import time 
from main import scrape_data
from config import *
from insert import main_insert
from vectordb import insert_main
import subprocess

st.title("Movie Database")

st.write("This database performs CRUD applications for movie reviews and LLM for question-answering")
val = st.text_input("Provide a movie or TV series along with year")
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

# st.button("Start the pipeline",help="It will submit the reviews that you selected to the database",on_click=click_button)
# if val!="":
#     start = time.time()
#     st.write("Started scraping data")
#     # scrape_data(val)

#     # st.write(f"The scraping took {round(time.time()-start,2)} seconds")
#     st.write(f"The scraping took {458.72} seconds")

#     st.write("Inserting the data to database and vector database")

#     start = time.time()
#     main_insert()
#     insert_main()
#     st.write(f"The insertion took {round(time.time()-start,2)} seconds")

#     st.write("Your database is ready to be used")
