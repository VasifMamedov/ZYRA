from src.ext import db
from src.models.base import BaseModel


class Actor(BaseModel):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    movies = db.relationship('Movie', back_populates='actors', secondary='actors_movies')
class ActorMovie(BaseModel):
    __tablename__ = 'actors_movies'
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
### ASSOCIATION TABLE ###

class Movie(BaseModel):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    actors = db.relationship('Actor', back_populates='movies', secondary = 'actors_movies')
users=[]