from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):
    title = TextAreaField ('Title of your blog')
    description = TextAreaField('Create a Blog', validators=[Required()])
    submit = SubmitField('Submit') 

class CommentForm(FlaskForm):
    comment = TextAreaField('write a comment',validators=[Required()])
    submit = SubmitField('comment')

    