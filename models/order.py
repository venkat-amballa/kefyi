from datetime import datetime
from db import db

from models.secondary_tables import ProductOrdersAssociation
from utils import date_format
from configs.constants import SALE_STATUS

class CustomerOrderModel(db.Model):

    __tablename__ = "orders"
    """
    Operations that billing db should support
    1. customer bills: Get bills of a particular user
    2. store bills : Get all the customer purchase bills for a store
    """
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(precision=3), nullable=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime,  server_default=db.func.now(), onupdate=db.func.now())

    # customer(parent)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id", ondelete="CASCADE"))
    customer = db.relationship("CustomerModel", back_populates="bills")
    # stores(parent)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.sid"))
    store = db.relationship('StoreModel', back_populates="orders")
    # wholesale, retail, custom
    sale_type = db.Column(db.String(20), nullable=False)
    # product(child)
    # products = db.relationship('ProductModel', secondary=products_bill, back_populates="bills_in")
    products = db.relationship('ProductOrdersAssociation', passive_deletes=True) # association table `ProductOrdersAssociation` is referenced here instead of `ProductModel`
    refunds = db.relationship('RefundsModel')

    status = db.Column(db.String(15), nullable=False)
    # isdebt = True # if payment type is pay later.
    # isactive = True # if the payment is pending.
    __table_args__ = (db.CheckConstraint(status.in_(SALE_STATUS)),)

    def __init__(self, customer_id, store_id, sale_type, status, amount) -> None:
        self.customer_id = customer_id
        self.store_id = store_id
        self.sale_type = sale_type
        self.status = status
        self.amount = amount

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "order_id": self.id,
            "customer_id": self.customer_id,
            "store_id": self.store_id,
            "sale_type": self.sale_type,
            "status": self.status,
            "amount": self.amount,
            "created_on": date_format(self.created_on),
            "updated_on": date_format(self.updated_on),
            # "products": [prod_order.product.json() for prod_order in self.products]
            "products": [prod_order.json() for prod_order in self.products],
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def products_in_order(cls, _id, _pids):
        return ProductOrdersAssociation.query.filter(ProductOrdersAssociation.order_id == _id)\
            .filter(ProductOrdersAssociation.product_id.in_(_pids)).all()
        # return cls.query.filter(cls.id == _id).filter(cls.products.id.in_(_pids)).all()
