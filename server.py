"""Server for movie ratings app."""

from flask import (Flask, render_template, jsonify, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

stars = '*' * 10


@app.route('/')
def show_homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def one_movie(movie_id):
    movie = crud.get_movie_by_id(movie_id)

    sum = 0
    for r in movie.ratings:
        sum += int(r.score)
    avg = sum / len(movie.ratings)

    return render_template('movie_details.html', movie=movie, avg=avg)

@app.route('/users')
def all_users():
    users = crud.get_users()
    return render_template('users.html', users=users)

@app.route('/users/<user_id>')
def one_user(user_id):
    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)

@app.route('/users', methods=['POST'])
def create_account():
    email = request.form.get('email')
    user = crud.get_user_by_email(email)

    if user:
        flash('''There is an account associated with that email.
        Please login.''')
    else:
        password = request.form.get('password')
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash('''Your account has been created.
        Please login now.''')

    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    email = request.form.get('email')
    user = crud.get_user_by_email(email)

    if session.get('name'):
        print(stars, session.get('user_id'))

    if user:
        password = request.form.get('password')
        if crud.check_password(email, password):
            session['user_id'] = user.user_id
            flash('Logged in!')
    else:
        flash('''There is no account associate with that email.
        Please sign up for an account.''')

    return redirect('/')

@app.route('/rate', methods = ['POST'])
def rate_movie():
    user = crud.get_user_by_id(session.get('user_id'))
    movie = crud.get_movie_by_id(int(request.form.get('movie_id')))
    print(stars, type(movie))
    score = int(request.form.get('score'))
    new_rating = crud.create_rating(user, movie, score)
    db.session.add(new_rating)
    db.session.commit()

    flash('Your rating has been recorded.')

    return redirect(request.referrer)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
