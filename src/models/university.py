from src.ext import db
from src.models.base import BaseModel

class University(BaseModel):
    __tablename__ = 'universities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    students = db.relationship('Student', back_populates='university')
class Student(BaseModel):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'))
    university = db.relationship('University', back_populates='students')