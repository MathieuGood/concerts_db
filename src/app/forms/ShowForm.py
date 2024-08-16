from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SelectField,
    SelectMultipleField,
    SubmitField,
    DateField,
    TextAreaField,
)
from wtforms.validators import DataRequired


class ShowForm(FlaskForm):
    name = StringField("Name", description="Name of the show")
    venue = SelectField(
        "Venue",
        description="Venue where the show took place",
        validators=[
            DataRequired(
                "A venue is needed to create a show, you cannot do without one"
            )
        ],
    )
    comments = TextAreaField("Comments", description="Comments related to the show")
    concerts = SelectMultipleField(
        "Concerts",
        description="All the concerts played at that specific show",
        validators=[DataRequired()],
    )
    submit = SubmitField(
        "Save show", description="Saves all the show details to the database"
    )
