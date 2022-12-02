"""CRUD operations"""

from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def get_users():
    """Returns all users in the database"""

    return User.query.all()


def get_user_by_id(id):
    """Returns one user by id"""
    return User.query.get(id)


def get_user_by_email(email):
    """Returns a user with a given email

    Returns None if the email is not in the db"""

    return User.query.filter(User.email == email).first()


def check_password(email, password):
    """Verifies user password at login

    Returns a boolean"""

    user = get_user_by_email(email)

    return user.password == password




def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(
        title=title,
        overview=overview,
        release_date=release_date,
        poster_path=poster_path
        )

    return movie


def get_movies():
    """Returns all movies in the database"""

    return Movie.query.all()


def get_movie_by_id(id):
    """Returns one movie by id"""
    return Movie.query.get(id)


def create_rating(user, movie, score):
    """Create and return a new rating."""

    rating = Rating(user=user, movie=movie, score=score)

    return rating


if __name__ == '__main__':
    from server import app
    connect_to_db(app)