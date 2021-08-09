from db import db
from models.secondary_tables import store_product


class StoreModel(db.Model):

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    # partner_id
    name = db.Column(db.String(100))
    address = db.Column(db.String(150))
    contact = db.Column(db.String(50))
    # user_id is the owner id of the store
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # foreign key
    products = db.relationship(
        "ProductModel", secondary=store_product, backref=db.backref("store", lazy=True)
    )

    orders = db.relationship("CustomerOrderModel", back_populates="store")
    # type = grocery, medical, clothes, electronic etc
    # id
    # name
    # manager_id
    # address
    # contact

    def __init__(self, user_id, name, address, contact):
        self.name = name
        self.address = address
        self.contact = contact
        self.user_id = user_id

    # insert new store(s) into db
    # delete new stor(e) from db
    # update a store
    # get details of a store(s)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def store_products(cls, _uid, _sid):
        """All products of a store"""
        res = cls.query.filter_by(user_id=_uid, id=_sid).first()
        if res:
            return res.products
        return res

    @classmethod
    def store_orders(cls, _uid, _sid):
        res = cls.query.filter_by(user_id=_uid, id=_sid).first()
        if res:
            return res.orders
        return res

    @classmethod
    def find_by_id(cls, _uid, _id):
        """ Find store_id for the given user"""
        return cls.query.filter_by(user_id=_uid, id=_id).first()

    @classmethod
    def find_by_user_id(cls, _uid):
        """
        Find all the stores for the user_id
        """
        return cls.query.filter_by(user_id=_uid).all()

    @classmethod
    def find_by_name(cls, _uid, name):
        return cls.query.filter_by(user_id=_uid, name=name).first()

    @classmethod
    def find_user_stores(cls, _uid):
        return cls.query.filter(user_id=_uid).all()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "contact": self.contact,
            "user_id": self.user_id,
        }

