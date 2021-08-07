from db import db

store_product = db.Table(
    "store_product",
    db.Column("store_id", db.Integer, db.ForeignKey("stores.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True),
)


# products_bill = db.Table('products_bill',
#     db.Column('bill_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
#     db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
# )


class ProductOrders(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), primary_key=True)
    price = db.Column(db.Float(precision=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship("ProductModel")

    def json(self):
        ordered_item = self.product.order_json()
        ordered_item["order_quantity"] = self.quantity
        ordered_item["order_price"] = self.price
        return ordered_item
