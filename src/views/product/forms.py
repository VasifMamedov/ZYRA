from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FloatField, TextAreaField, IntegerField, SelectField, MultipleFileField
from wtforms.validators import Optional, NumberRange
from flask_wtf.file import FileAllowed, FileField
from flask_babel import lazy_gettext as _l

class ProductForm(FlaskForm):
    name = StringField(_l("Product Name"))
    price = FloatField(_l("Product Price"))
    img = FileField(_l("Main Image"), validators=[FileAllowed(['jpg', 'png', 'jpeg', 'heic'], _l('Images only!'))])
    extra_images = MultipleFileField(_l("Additional Images"))
    description = TextAreaField(_l("Product Description"), validators=[Optional()])
    stock = IntegerField(_l("Stock"), validators=[Optional(), NumberRange(min=0)], default=0)
    category_id = SelectField(_l("Category"), coerce=int, validators=[Optional()])
    submit = SubmitField(_l('Save'))