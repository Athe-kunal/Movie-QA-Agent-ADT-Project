## STEPS TO RUN AND EXTRACT THE DATA

First create a virtual environment and activate it

```
python -m venv imdb-movie

source imdb-movie/bin/activate
```

Then install all the dependencies

```
pip install -r requirements.txt
```

For a movie, pass the year and date in the command to save the the csv file in `movie_reviews_link` folder

```
python main.py ---movie_name="Angry Birds 2016"  
```

To insert the data to MongoDB cluster, run

```
python insert.py
```

TO-DOS
1. Data collection (Astarag) (Done) and Upload the data to MongoDB cluster
2. CRUD: Read (rating, date, plot data) (C&D). Update the newer reviews from IMDB or wikipedia (A) [cuss words [NONE]], delete (C&D) (delete cuss words movie reviews and irrelevant reviews (helpful=0 and total votes = 0 and length of review is less than 20))
3. LLM (Astarag and Diskha)
4. Frontend(without LLM) and deployment(Chandu) UX design
5. Frontend with LLM (Diksha)

Application
1. Distribution of ratings (Pie chart) (D)
2. Wordcloud (D)
3. Most recent reviews (D)
4. Most helpful reviews (top-10) (C)
5. Spoiler based reviews (C)
6. Keyword based filtering (C)
7. LLM Chat agent