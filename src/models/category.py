from src.ext import db
from src.models.base import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    name_tr = db.Column(db.String, nullable=True)
    name_ka = db.Column(db.String, nullable=True)

    products = db.relationship('Product', secondary='product_categories', back_populates='category')

    def __repr__(self):
        return self.name

class ProductCategory(BaseModel):
    __tablename__ = 'product_categories'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
