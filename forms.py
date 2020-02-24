from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    actors = TextAreaField('Actors (one per line please)', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    image = StringField('Image Link (full path)', validators=[DataRequired()])
    submit = SubmitField('Add Review')


class EditReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    actors = TextAreaField('Actors (one per line please)', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    image = StringField('Image Link (full path)', validators=[DataRequired()])
    submit = SubmitField('Update Review ')


class ConfirmDelete(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Delete this Review')