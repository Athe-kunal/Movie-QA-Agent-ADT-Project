import streamlit as st
from chat import qA_movie
import time
import openai
from config import *
from dotenv import load_dotenv
from pymongo import MongoClient
import pymongo
import os
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.embeddings import SentenceTransformerEmbeddings

st.title("Movie QA")


load_dotenv()

# initialize MongoDB python client
client = MongoClient(MONGODB_CLUSTER)
MONGODB_COLLECTION = client[DATABASE_NAME][VECTORDB_COLLECTION_NAME]

some_key  = os.environ["KY"]
some_key = "sk-" + some_key + "88y1A"
openai.api_key = some_key

vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    MONGODB_CLUSTER,
    DATABASE_NAME + "." + VECTORDB_COLLECTION_NAME,
    SentenceTransformerEmbeddings(model_kwargs={"device": "cuda"}),
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

def generate_response(input_text):
    return qA_movie(input_text,vector_search)


if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hi, how can I help you?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input():
    # Display user message in chat message container
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Answering..."):
            docs = generate_response(prompt) 
            print(docs)
            st.write(docs["result"]) 
            expander = st.expander("See relevant IMDB movie review links")
            citation_links = [doc.metadata['link'] for doc in docs['source_documents']]
            sources_text = ""
            for idx,link in enumerate(citation_links):
                sources_text+=f"[Source Link {idx}]({link})"
                sources_text+="\n\n"
            expander.write(sources_text)
    message = {"role": "assistant", "content": docs['result']}
    st.session_state.messages.append(message)