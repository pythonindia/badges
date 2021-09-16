import re

from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField
from wtforms import Field, IntegerField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    NumberRange,
    Length,
    ValidationError,
    url,
    UUID,
)


class VerifyEmailForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Verify!")


def get_id_checker(field_name: str, length: int=None):
    def id_checker(form: FlaskForm, field: Field) -> bool:
        if not field.data:
            raise ValidationError(f"{field_name} cannot be empty.")

        try:
            if length and len(field.data) > length:
                raise ValidationError(f"{field_name} entered is invalid")

            int(field.data)
            if int(field.data) < 0:
                raise
        except:
            raise ValidationError(f"{field_name} entered is invalid.")

    return id_checker


class VerifyRegistrationForm(FlaskForm):
    booking_id = StringField("Booking ID", validators=[get_id_checker("Booking ID")])
    token = StringField(
        "Token",
        validators=[
            DataRequired(message="Token cannot be empty."),
            UUID(message="The token is invalid."),
        ],
    )
    submit = SubmitField("Get my badge!")


class VerifyRegistrationByOrderForm(FlaskForm):
    booking_id = StringField("Booking ID", validators=[get_id_checker("Booking ID", 7)])
    order_id = StringField("Order ID", validators=[get_id_checker("Order ID")],)
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
