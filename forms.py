from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, URL


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=5000)])
    image_url = StringField('Image URL', validators=[Optional(), URL(require_tld=False), Length(max=500)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
