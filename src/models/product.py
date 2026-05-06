from src.ext import db
from src.models.base import BaseModel

class Product(BaseModel):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    img = db.Column(db.String)
    description = db.Column(db.Text, nullable=True)
    stock = db.Column(db.Integer, default=0)
    #category_id = db.Column(db.Integer, db.ForeignKey('categories.id', name='fk_product_category'), nullable=True)

    category = db.relationship('Category', secondary='product_categories', back_populates='products')
    users = db.relationship("User", back_populates="products", secondary="favorites")
    images = db.relationship('Image', back_populates='product', cascade='all, delete-orphan')
    def __repr__(self):
        return self.name