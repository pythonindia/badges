import re

from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField
from wtforms import Field, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, url


class VerifyEmailForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    submit = SubmitField("Verify!")


class VerifyRegistrationForm(FlaskForm):
    booking_id = IntegerField("booking_id", validators=[DataRequired()])
    token = StringField("token", validators=[DataRequired()])
    submit = SubmitField("Get my badge!")


def username_check(form: FlaskForm, field: Field) -> bool:
    username_pattern = r"^[a-z-]+$"

    if not bool(re.match(username_pattern, field.data)):
        raise ValidationError(
            "Username should contain only lower case characters and hyphen"
        )


class BadgeForm(FlaskForm):
    fullname = StringField("fullname", validators=[DataRequired()])
    avatar_url = URLField("avatar_url", validators=[url()])
    twitter_id = StringField("twitter_id")
    username = StringField("username", validators=[username_check])
    about = StringField(
        "about",
        validators=[
            Length(max=80, message="About section needs to be less than 80 characters")
        ],
    )
    submit = SubmitField("Save")
