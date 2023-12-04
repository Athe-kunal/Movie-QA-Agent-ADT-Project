import streamlit as st
import time 
from main import scrape_data
from config import *
from insert import main_insert
from vectordb import insert_main
st.title("Movie Database")

val = st.text_input("Provie a movie or TV series along with year")

start = time.time()
st.write("Started scraping data")
scrape_data(val)

st.write(f"The scraping took {round(time.time()-start,2)} seconds")

st.write("Inserting the data to database and vector database")

start = time.time()
main_insert()
insert_main()
st.write(f"The insertion took {round(time.time()-start,2)} seconds")

st.write("Your database is ready to be used")
