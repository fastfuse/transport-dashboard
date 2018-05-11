from app import db


class Stop(db.Model):
    """
    Model represents Public Transport Stop.
    """

    __tablename__ = "stops"

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    internal_id = db.Column('internal_id', db.String)
    name = db.Column('name', db.Unicode)
    code = db.Column('code', db.String)
    # location = db.Column('location', db.String)
