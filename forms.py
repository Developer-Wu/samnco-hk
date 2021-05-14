from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
class SearchBar(FlaskForm):
    query = StringField('', validators=[DataRequired()])
    search_btn = SubmitField('Search')
