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

    def __init__(self, internal_id, name, code):
        self.internal_id = internal_id
        self.name = name
        self.code = code
