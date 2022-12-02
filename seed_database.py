"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)
model.db.create_all()


# Load movie data from JSON file
with open("data/movies.json") as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
db_movies = []
for m in movie_data:
    title = m['title']
    overview = m['overview']
    rel_date = datetime.strptime(m['release_date'], "%Y-%m-%d")
    poster_path = m['poster_path']

    db_movie = crud.create_movie(title, overview, rel_date, poster_path)
    db_movies.append(db_movie)

model.db.session.add_all(db_movies)
model.db.session.commit()


# Create random users
rand_users = []
for n in range(10):
    email = f"user{n}@email.com"
    password = 'abc123'

    user = crud.create_user(email, password)
    rand_users.append(user)

    user_ratings = []
    for n in range(10):
        movie = choice(db_movies)
        score = randint(1, 5)

        rating = crud.create_rating(user, movie, score)
        user_ratings.append(rating)

    model.db.session.add_all(user_ratings)

model.db.session.add_all(rand_users)
model.db.session.commit()