import re

from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField
from wtforms import Field, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, url


class VerifyEmailForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Verify!")


class VerifyRegistrationForm(FlaskForm):
    booking_id = IntegerField("Booking ID", validators=[DataRequired()])
    token = StringField("Token", validators=[DataRequired()])
    submit = SubmitField("Get my badge!")


def username_check(form: FlaskForm, field: Field) -> bool:
    username_pattern = r"^[a-z-]+$"

    if not bool(re.match(username_pattern, field.data)):
        raise ValidationError(
            "Username should contain only lower case characters and hyphen"
        )


class BadgeForm(FlaskForm):
    fullname = StringField(
        "Full Name",
        description="Your name that should be visible on the badge",
        validators=[DataRequired()],
    )
    avatar_url = URLField(
        "Avatar URL",
        description="A link to the image that you want as your photo on the badge. The image ideally should be of 1:1 aspect ratio.",
        validators=[url()],
    )
    twitter_id = StringField("Twitter ID", description="Your Twitter ID")
    username = StringField(
        "Username",
        description="By default, your username is a random ID. If you want a custom name in your badge URL, please put in here. Only lower case alphabets and hyphen '-' are allowed in this field. Please note that the usernames are First Come First Serve.",
        validators=[username_check],
    )
    about = StringField(
        "About",
        description="Write something unique about you",
        validators=[
            Length(max=80, message="About section needs to be less than 80 characters")
        ],
    )
    submit = SubmitField("Save")
