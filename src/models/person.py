from src.ext import db
from src.models.base import BaseModel

class Person(BaseModel):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    birth_date = db.Column(db.Date)
    idcard_id = db.Column(db.Integer, db.ForeignKey('id_cards.id'))
    idcard = db.relationship('IDCard', back_populates='person')

class IDCard(BaseModel):
    __tablename__ = 'id_cards'
    id = db.Column(db.Integer, primary_key=True)
    personal_number = db.Column(db.String)
    serial_number = db.Column(db.String)
    expiration_date = db.Column(db.Date)
    person = db.relationship('Person', back_populates='idcard', uselist=False)