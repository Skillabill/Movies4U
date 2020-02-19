from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class CreateRecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    actors = TextAreaField('Actorss (one per line please)', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    image = StringField('Image Link (full path)', validators=[DataRequired()])
    submit = SubmitField('Add Recipe')


class EditRecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    actors = TextAreaField('Actorss (one per line please)', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    image = StringField('Image Link (full path)', validators=[DataRequired()])
    submit = SubmitField('Update Review ')


class ConfirmDelete(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Delete this Recipe')