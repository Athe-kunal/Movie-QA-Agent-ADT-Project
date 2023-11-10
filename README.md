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

For a movie, pass the year and date in the command to save the the csv file in `movie_reviews` folder

```
python main.py ---movie_name="Angry Birds 2016"  
```