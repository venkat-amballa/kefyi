from db import db

store_product = db.Table('store_product',
    db.Column('store_id', db.Integer, db.ForeignKey('stores.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)