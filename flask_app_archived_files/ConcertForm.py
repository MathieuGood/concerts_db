from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    SelectMultipleField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired


class Concerts(FlaskForm):

    def __init__(self, artists: list[str]) -> None:
        super().__init__()
        self.venue.choices = artists

    artist = SelectField(
        "Artist", description="Name of the artist", validators=[DataRequired()]
    )
    setlist = TextAreaField("Setlist", description="Setlist of the concert")
    comments = TextAreaField("Comments", description="Comments related to the concert")
    images = SelectMultipleField("Images", description="Images of the concert")
    videos = SelectMultipleField("Videos", description="Videos of the concert")
    submit = SubmitField(
        "Save concert", description="Saves all the concert details to the database"
    )
