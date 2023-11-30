from config import *
from dotenv import load_dotenv
import os
import openai
from pymongo import MongoClient
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

load_dotenv()

# initialize MongoDB python client
client = MongoClient(MONGODB_CLUSTER)
MONGODB_COLLECTION = client[DATABASE_NAME][VECTORDB_COLLECTION_NAME]

openai.api_key = os.environ["OPENAI_API_KEY"]

def qA_movie(query:str):
    vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    MONGODB_CLUSTER,
    DATABASE_NAME + "." + VECTORDB_COLLECTION_NAME,
    SentenceTransformerEmbeddings(model_kwargs={"device": "cuda"}),
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    qa_retriever = vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 100, "post_filter_pipeline": [{"$limit": 5}]},
    )

    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    """
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=qa_retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},
    )

    docs = qa({"query": query})

    # print(docs["result"])
    # print(docs["source_documents"])
    return docs