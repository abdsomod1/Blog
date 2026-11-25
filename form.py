from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired, InputRequired, Regexp, Length

class PostForm (FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content',
                            validators=[DataRequired(),
                            Length (max=500, message= 'cannot be above 500 letter')])
    category = SelectField(
    'Category',
    coerce=int
    )
    

