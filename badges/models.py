from typing import TypeVar, Union
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from psycopg2.errors import UniqueViolation
from sqlalchemy.dialects.postgresql import TEXT, UUID

from badges import db

Attendee = TypeVar("Attendee")


class Attendee(db.Model):
    uuid = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    token = db.Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False,)
    booking_id = db.Column(db.Integer, unique=True, index=True, nullable=False)
    email = db.Column(TEXT, index=True, nullable=False)
    fullname = db.Column(TEXT, nullable=False)
    avatar_url = db.Column(TEXT, nullable=False, default="https://www.gravatar.com/avatar/00000000000000000000000000000000")
    username = db.Column(TEXT, index=True)
    twitter_id = db.Column(TEXT)
    about = db.Column(TEXT)

    @property
    def id(self) -> str:
        return self.username or self.uuid

    def update(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<Attendee {}>".format(self.uuid)

    @classmethod
    def create(cls, booking_id: int, email: str, fullname: str) -> Attendee:
        a = Attendee(booking_id=booking_id, email=email, fullname=fullname)
        db.session.add(a)
        db.session.commit()

        return a

    @classmethod
    def find_by_id(cls, id: str) -> Union[Attendee, None]:
        # first search by username
        a = cls.query.filter_by(username=id).first()

        if a:
            return a

        # search by uuid id username is not set yet
        return cls.query.filter_by(uuid=id).first()

    @classmethod
    def find_by_uuid(cls, uuid: str) -> Union[Attendee, None]:
        return cls.query.filter_by(uuid=uuid).first()

    @classmethod
    def find_by_email(cls, email: str) -> Union[Attendee, None]:
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_booking_id(cls, booking_id: str) -> Union[Attendee, None]:
        return cls.query.filter_by(booking_id=booking_id).first()

    @classmethod
    def verify(cls, booking_id: int, token: str) -> bool:
        a = cls.find_by_booking_id(booking_id=booking_id)
        if a and str(a.token) == token:
            return True

        return False
