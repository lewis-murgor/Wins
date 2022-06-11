from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,RadioField,SelectField,ValidationError
from wtforms.validators import InputRequired,Email

class UpdateProfile(FlaskForm):
    
    bio = TextAreaField('Tell us about you.',validators = [InputRequired()])
    submit = SubmitField('Submit')

class WinForm(FlaskForm):

    title = StringField('Title')
    text = TextAreaField('Win')
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):

    comment = TextAreaField('Comment')
    submit = SubmitField('Submit')