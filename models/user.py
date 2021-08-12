from db import db
from utils import date_format


class UserModel(db.Model):
    """
    User Model, this user has ownership of one/mutiple stores.
    misc columns: stores []
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80))
    password = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200))
    email = db.Column(db.String(80))
    mobile = db.Column(db.String(20), nullable=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    stores = db.relationship("StoreModel", backref="user_owner")

    def __init__(
        self, username, first_name, last_name, password, address, email, mobile
    ):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.address = address
        self.email = email
        self.mobile = mobile

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        email = self.email.split("@")
        mobile = self.mobile
        mobile = "********" + mobile[-2:]
        email = ("******" + email[0][-2:] + "@" + email[1],)
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": email,
            "mobile": mobile,
            "created_on": date_format(self.created_on),
        }

    @classmethod
    def find_by_id(cls, _id):
        """
        Find the given in the db
        """
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_first_name(cls, first_name):
        """
        Find the given in the db
        """
        return cls.query.filter_by(first_name=first_name).first()

    @classmethod
    def find_by_username(cls, username):
        """
        Find the given in the db
        """
        return cls.query.filter_by(username=username).first()
