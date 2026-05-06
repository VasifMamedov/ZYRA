from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FloatField, TextAreaField, IntegerField, SelectField, MultipleFileField
from wtforms.validators import Optional, NumberRange
from flask_wtf.file import FileAllowed, FileField

class ProductForm(FlaskForm):
    name = StringField("Product Name")
    price = FloatField("Product Price")
    img = FileField("Main Image", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'heic'], 'Images only!')])
    extra_images = MultipleFileField("Additional Images")
    description = TextAreaField("Product Description", validators=[Optional()])
    stock = IntegerField("Stock", validators=[Optional(), NumberRange(min=0)], default=0)
    category_id = SelectField("Category", coerce=int, validators=[Optional()])

    submit = SubmitField('Save')