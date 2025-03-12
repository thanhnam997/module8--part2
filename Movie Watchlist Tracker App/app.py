# Importing the modules
# Render_template renders HTML, request handles form data
# Redirect and url_for direct users to a route in the website navigation
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    release_year = db.Column(db.Integer)
    watched = db.Column(db.Boolean, default=False)

# Home route - List all movies
@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template("index.html", movies=movies)

# Add a new movie
@app.route('/add', methods=['POST'])
def add_movie():
    title = request.form["title"]
    genre = request.form["genre"]
    year = request.form["year"]
    new_movie = Movie(title=title, genre=genre, release_year=year)
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('index'))

# Mark as watched
@app.route('/watch/<int:id>')
def mark_watched(id):
    movie = Movie.query.get(id)
    if movie:
        movie.watched = True
        db.session.commit()
    return redirect(url_for('index'))

# Delete a movie
@app.route('/delete/<int:id>')
def delete_movie(id):
    movie = Movie.query.get(id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
