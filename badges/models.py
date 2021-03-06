import re
from typing import TypeVar, Union
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from psycopg2.errors import UniqueViolation
from sqlalchemy.dialects.postgresql import TEXT, UUID

from badges import db

Attendee = TypeVar("Attendee")


UUID_PATTERN = re.compile(r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$", re.IGNORECASE)
VALID_ATTENDEE_TYPES = ["attendee", "speaker", "volunteer"]


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
    avatar_url = db.Column(
        TEXT,
        nullable=False,
        default="https://www.gravatar.com/avatar/00000000000000000000000000000000",
    )
    username = db.Column(TEXT, index=True)
    twitter_id = db.Column(TEXT)
    about = db.Column(TEXT)
    ticket_type = db.Column(TEXT)
    type = db.Column(TEXT, default="attendee")
    order_id = db.Column(TEXT, nullable=False)

    @property
    def id(self) -> str:
        return self.username or self.uuid

    def set_type(self, type: str):
        if type not in VALID_ATTENDEE_TYPES:
            raise ValueError(
                "Attendee type has to be one of {}".format(
                    ", ".join(VALID_ATTENDEE_TYPES)
                )
            )

        self.type = type
        self.update()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<Attendee {}>".format(self.uuid)

    @classmethod
    def create(
        cls, booking_id: int, order_id: int, email: str, fullname: str, ticket_type: str
    ) -> Attendee:
        a = Attendee(
            booking_id=booking_id,
            order_id=order_id,
            ticket_type=ticket_type,
            email=email,
            fullname=fullname,
        )
        db.session.add(a)
        db.session.commit()

        return a

    @classmethod
    def find_by_id(cls, id: str) -> Union[Attendee, None]:
        # first search by username
        a = cls.query.filter_by(username=id).first()

        if a:
            return a

        try:
            UUID(id)
        except ValueError:
            return

        if not UUID_PATTERN.match(id):
            return

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
    def verify(cls, booking_id: int, *, order_id: int = 0, token: str = "") -> bool:
        a = cls.find_by_booking_id(booking_id=booking_id)
        if a and token and str(a.token) == token:
            return True

        if a and order_id or a.order_id == order_id:
            return True

        return False
