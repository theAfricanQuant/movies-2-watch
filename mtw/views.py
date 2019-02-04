from flask import render_template, flash, url_for, redirect, request
from mtw import app, db, bcrypt, mail
from mtw.forms import RegistrationForm, LoginForm, AddMovie, RequestResetForm, ResetPasswordForm, SearchForMovie, AddMovieFromSearch
from mtw.models import User, Movie, load_user
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from config import Omdb
from omdb import OMDBClient


@app.route('/')
def index():
    ''' Root route '''
    if current_user.is_authenticated:
        return redirect(url_for('movies'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' Login route '''
    if current_user.is_authenticated:
        return redirect(url_for('movies'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('movies'))
        else:
            flash('Login unsuccessful. Please check your email and password and try again', 'info')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    ''' Logout route '''
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    ''' Register new User route '''
    if current_user.is_authenticated:
        return redirect(url_for('movies'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/movies', methods=['GET', 'POST'])
@login_required
def movies():
    ''' Route for the users main movies list '''
    movies = Movie.query.filter_by(owner_id=current_user.id)
    return render_template('movies.html', movies=movies)


@app.route('/movies/new', methods=['GET', 'POST'])
@login_required
def new_movie():
    ''' Manually add a new movie route '''
    form = AddMovie()
    if form.validate_on_submit():
        film = Movie(title=form.title.data, year_released=form.year_released.data, owner_id=current_user.id)
        db.session.add(film)
        db.session.commit()
        flash(f'You have successfully added the movie: {film.title}!', 'success')
        return redirect(url_for('movies'))
    return render_template('new-movie.html', form=form)


@app.route('/movies/delete/<movieid>', methods=['GET', 'POST'])
@login_required
def delete(movieid):
    ''' Deletes an movie from the users list '''
    film = Movie.query.get_or_404(movieid)
    if request.method == 'POST':
        db.session.delete(film)
        db.session.commit()
        flash(f'{film.title} has been deleted', 'success')
        return redirect(url_for('movies'))
    return render_template('delete-movie.html', movie=film)


# Send Password Reset Email
def send_reset_email(user):
    ''' Sends Email '''
    token = user.get_reset_token()
    # TODO: Change the sender email to valid email address
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset you password visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request simply ignore this email.
'''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    ''' User password request reset route '''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with your password reset instructions', 'info')
        return redirect(url_for('login'))
    return render_template('reset-request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    ''' Route for password reset acquired from reset email '''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset-token.html', form=form)


@app.route('/movies/search', methods=['GET','POST'])
def search_movie():
    ''' Searches for a movie to add to the list '''
    form = SearchForMovie()
         
    if form.validate_on_submit():
        results = []
        client = OMDBClient(apikey=Omdb.OMDB_KEY)
        search = client.search_movie(form.search.data)
        for s in search:
            title = s['title']
            year = s['year']
            movie = client.get(title=title, year=year, fullplot=False)
            results.append(movie)
        return render_template('search.html', results=results, form=form)
                
    return render_template('search.html', form=form)


@app.route('/movies/search/add/', methods=['GET', 'POST'])
def add_from_search():
    ''' Adds Movie from the Search Results '''
    if request.method == 'POST':
        addform = AddMovieFromSearch()
        print(addform.data)
        film = Movie(title=addform.title.data, year_released=addform.year_released.data, owner_id=current_user.id)
        db.session.add(film)
        db.session.commit()
        flash(f'You have successfully added the movie: {film.title}!', 'success')
        return redirect(url_for('movies'))
