import streamlit as st
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import certifi
from wordcloud import WordCloud
from config import MONGODB_CLUSTER, DATABASE_NAME, COLLECTION_NAME

# Connect to MongoDB
client = MongoClient(MONGODB_CLUSTER, tlsCAFile=certifi.where())
db = client[DATABASE_NAME]
ratings_collection = db[COLLECTION_NAME]

# Get distinct movie names from the database
distinct_movie_names = ratings_collection.distinct("MovieName")

# Streamlit App
st.title("Movie Information")

# Get user input for movie name and user words
movie_name = st.selectbox("Select Movie Name:", distinct_movie_names, key="movie_input")
user_words = st.text_input("Enter Comma-Separated Words:")

# Button to show ratings distribution
if st.button("Show Results"):

    if not movie_name:
        st.warning("Please select a movie name.")
    elif not user_words:
        st.warning("Please enter comma-separated words.")
    else:
        # Query MongoDB for ratings
        ratings_data = list(ratings_collection.find({"MovieName": movie_name}))

        if not ratings_data:
            st.warning("No data found for the selected movie.")
        else:
            # Create DataFrame from MongoDB data
            df = pd.DataFrame(ratings_data)

            # Display the title for Rating Distribution
            st.title('Rating Distribution')

            # Plot pie chart using matplotlib
            fig, ax = plt.subplots()
            
            ax.pie(df['rating'].value_counts(), labels=df['rating'].value_counts().index,
            autopct=lambda p: '{:.1f}%'.format(p), startangle=0, colors=plt.cm.Paired.colors,
            textprops={'fontsize': 8})  # Adjust the fontsize value as needed

            ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

            # Show the plot in Streamlit
            st.pyplot(fig)

            # Generate word cloud based on the text
            text_corpus = ' '.join(df['comment'].astype(str))
            wordcloud = WordCloud(width=800, height=400, background_color='black').generate(text_corpus)

            # Display the word cloud
            st.title('Word Cloud based on Reviews')
            st.image(wordcloud.to_array(), caption=f'Word Cloud for {movie_name}', width=800)

            # Display the top 10 recent texts in a table without index column
            st.title('Top 10 Recent Reviews')
            top_texts_df = df.sort_values(by='date', ascending=False).head(10)[['date', 'comment']]
            st.write(top_texts_df.style.set_properties(**{'text-align': 'left'}))

            st.title('Number of Reviews per Year')
            df['year'] = pd.to_datetime(df['date']).dt.year
            reviews_per_year = df['year'].value_counts().sort_index()

            # Plot bar chart using matplotlib
            fig_bar, ax_bar = plt.subplots()
            ax_bar.bar(reviews_per_year.index, reviews_per_year.values, color='skyblue')
            ax_bar.set_xlabel('Year')
            ax_bar.set_ylabel('Number of Reviews')
            st.pyplot(fig_bar)

            # Display the table for top 10 texts based on 'helpful'
            st.title('Top 10 Reviews based on Helpful Votes')
            top_helpful_df = df.sort_values(by='helpful', ascending=False).head(10)[['date', 'comment', 'helpful']]
            st.write(top_helpful_df.style.set_properties(**{'text-align': 'left'}))
            
            # Split user input into a list of words
            user_word_list = [word.strip() for word in user_words.split(',')]

            # Filter DataFrame based on user words
            filtered_df = df[df['comment'].str.contains('|'.join(user_word_list), case=False, na=False)]

            # Display a table with text and total_votes for the top 10 texts
            st.title(f'Top 10 Reviews Containing Words: {", ".join(user_word_list)}')
            top_user_words_df = filtered_df.sort_values(by='total_votes', ascending=False).head(10)[['comment', 'total_votes']]
            st.write(top_user_words_df.style.set_properties(**{'text-align': 'left'}))

# Create an empty container for dynamic updates
container = st.empty()

def reset_conversation():
    st.session_state.movie_name = None
    container.empty()

st.button('Reset Input', on_click=reset_conversation)
