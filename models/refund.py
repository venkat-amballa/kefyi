from db import db


class RefundsModel(db.Model):
    __tablename__ = "refunds"
    # refund_id
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    amount = db.Column(db.Float(precision=2), nullable=False)
    return_items = db.relationship("ProductRefundAssociation")

    def __init__(self, order_id, amount):
        self.order_id = order_id
        self.amount = amount

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


