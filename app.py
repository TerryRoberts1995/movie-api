from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')


db = SQLAlchemy(app)
ma = Marshmallow(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20))
    description = db.Column(db.String(144))
    rating = db.Column(db.Integer)
    genre = db.Column(db.String(15))

    def __init__(self,title, description,rating,genre):
        self.title = title
        self.description = description
        self.rating = rating
        self.genre = genre

class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id','title', 'description','rating','genre')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many = True)

@app.route('/movie', methods = ['POST'])
def create_movie():
    
    title = request.json['title']
    description = request.json['description']
    rating = request.json['rating']
    genre = request.json['genre']

    new_movie = Movie(title,description, rating, genre)

    db.session.add(new_movie)
    db.session.commit()

    return movie_schema.jsonify(new_movie)

# End point to create a new movie

@app.route('/movies', methods = ['GET'])
def get_movies():

    movies = Movie.query.all()
    result = movies_schema.dump(movies)
    
    return jsonify(result)

#  End point to get all movies


@app.route('/movie/<id>', methods = ['GET'])
def get_movie(id):

    movie  = Movie.query.get(id)

    return movie_schema.jsonify(movie)

#  End point to get a movie

@app.route("/movie/<id>", methods=["DELETE"])
def delete_movie(id):
    movie = Movie.query.get(id)
    
    db.session.delete(movie)
    db.session.commit()

    return movie_schema.jsonify(movie)

#  End point for deleting a movie

if __name__ == '__main__':
    app.run(debug = True)

