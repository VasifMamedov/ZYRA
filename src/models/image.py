from src.ext import db
from src.models.base import BaseModel

class Image(BaseModel):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', name='fk_productimage_product'), nullable=False)
    img = db.Column(db.String, nullable=False)

    product = db.relationship('Product', back_populates='images')