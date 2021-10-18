from db import db
from utils import date_format


class CustomerModel(db.Model):
    """
    Customer Model, This custmer buys products from a store
    v1: Buys from a store, No password required as the store owner makes the bill,
        for the customer.
        - No username, password
    v2: Buys online, The bill will be generated after successful transaction. He has his own identity
        i.e, they have their own username, password.
    """

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    # username =  db.Column(db.String(80)) # nullable=False, unique=True
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    # password = db.Column(db.String(80)) # nullable=False
    address = db.Column(db.String(200))
    email = db.Column(db.String(80))
    mobile = db.Column(db.String(20), nullable=False, unique=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    bills = db.relationship("CustomerOrderModel", back_populates="customer", passive_deletes=True)

    def __init__(self, mobile, first_name=None, last_name=None, address=None, email=None):
        self.first_name = first_name
        self.last_name = last_name
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
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "mobile": self.mobile,
            "created_on": date_format(self.created_on),
            "updated_on": date_format(self.updated_on),
        }

    @classmethod
    def orders(cls, _cid):
        return cls.query.filter_by(id=_cid).scalar().bills
        # return cls.query.filter_by(mobile_no=mobile_no).scalar().bills

    @classmethod
    def find_by_id(cls, _id):
        """
        Find the given in the db
        """
        return cls.query.filter_by(id=_id).scalar()

    @classmethod
    def find_by_first_name(cls, first_name):
        """
        Find the given in the db
        """
        return cls.query.filter_by(first_name=first_name).first()

    @classmethod
    def find_by_mobile(cls, mobile):
        """
        Find the given in the db
        """
        return cls.query.filter_by(mobile=mobile).first()

    @classmethod
    def find_by_email(cls, email):
        """
        Find the given in the db
        """
        return cls.query.filter_by(email=email).first()
