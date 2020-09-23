import os


class Config:
    SECRET_KEY = (
        os.getenv("SECRET_KEY")
        or "equity~reprogram~unworried~splendid~deviation~width~pungent~awkward"
    )
    SQLALCHEMY_DATABASE_URI = os.getenv("BADGES_DSN") or "postgres:///badges"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    URL_PREFIX = os.getenv("URL_PREFIX") or ""
