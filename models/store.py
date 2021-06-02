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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # foreign key
    products = db.relationship('ProductModel', secondary=store_product, backref = db.backref('stores',  lazy=True))
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
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "contact": self.contact,
            "products": [product.json() for product in self.products],
            "user_id":self.user_id
        }
