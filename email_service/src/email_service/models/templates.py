from email_service.models import db


class Templates(db.Model):
    __tablename__ = "templates"

    name = db.Column(db.Unicode())
    body = db.Column(db.Unicode())

