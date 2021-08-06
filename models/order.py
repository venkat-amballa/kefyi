from datetime import datetime
from db import db

from models.secondary_tables import ProductOrders

class CustomerOrderModel(db.Model):
    
    __tablename__ = "orders"

    '''
    Operations that billing db should support
    1. customer bills: Get bills of a particular user
    2. store bills : Get all the customer purchase bills for a store
    '''
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(precision=3), nullable=False)
    # customer(parent)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    customer = db.relationship('CustomerModel', back_populates="bills")
    
    # stores(parent)
    store_id  = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship('StoreModel', back_populates="orders")
    # wholesale, retail, custom
    sale_type = db.Column(db.String(20), nullable=False)
    # product(child)
    # products = db.relationship('ProductModel', secondary=products_bill, back_populates="bills_in")
    products = db.relationship('ProductOrders') # association table `ProductOrders` is referenced here instead of `ProductModel`

    status = db.Column(db.String(1), nullable=False)
    # isdebt = True # if payment type is paylater.
    # isactive = True # if the payment is pending.
    # status = ["success", "failure", "pending"]

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
            "customer_id":self.customer_id,
            "store_id":self.store_id,
            "sale_type":self.sale_type,
            "status":self.status,
            "amount":self.amount,
            # "products": [prod_order.product.json() for prod_order in self.products]
            "products": [prod_order.json() for prod_order in self.products]
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()



