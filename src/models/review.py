from datetime import datetime
from src.ext import db
from src.models.base import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_review_user'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', name='fk_review_product'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='reviews')
    product = db.relationship('Product', backref=db.backref('reviews', cascade='all, delete-orphan'))