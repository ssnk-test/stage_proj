from app_mon.models import db

class Event(db.Model):
    __tablename__ = "events"

    service = db.Column(db.Unicode())
    url = db.Column(db.Unicode())
    status = db.Column(db.Unicode())
    req_time = db.Column(db.Unicode())
    res_time = db.Column(db.Unicode())
