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
1. Data collection (Astarag)
2. CRUD: Read (rating, movie, date, spoiler filters, plot data). Update the newer reviews from IMDB or wikipedia, delete (delete cuss words movie reviews)
3. LLM (Astarag and Diskha)
4. Frontend and deployment(Chandu) UX design

Application
1. Distribution of ratings (Pie chart)
2. Wordcloud
3. Most recent reviews
4. Most helpful reviews (top-10)
5. Spoiler based reviews
6. Keyword based filtering
7. LLM Chat agent