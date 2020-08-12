from . import db


class Templates(db.Model):
    __tablename__ = "templates"

    name = db.Column(db.Unicode())
    body = db.Column(db.Unicode())

