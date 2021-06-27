from db import db

store_product = db.Table('store_product',
    db.Column('store_id', db.Integer, db.ForeignKey('stores.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

products_bill = db.Table('products_bill',
    db.Column('bill_id', db.Integer, db.ForeignKey('customerbills.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('price', db.Float(precision=3))
)


