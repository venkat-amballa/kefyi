# from db import db

# class StoreProducts(db.Model):

#     __tablename__ = "storeproducts"

#     id = db.Column(db.Integer, primary_key=True)
#     store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
#     wholesale_price = db.Column(db.Float(precision=3), nullable=False)
#     retail_price = db.Column(db.Float(precision=3), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     # manufactured_on = 
#     # expires_on = 


#     def __init__(self, store_id, product_id, wholesale_price, retail_price, quantity):
#         self.store_id = store_id
#         self.product_id = product_id
#         self.wholesale_price = wholesale_price
#         self.retail_price = retail_price
#         self.quantity = quantity
    
#     def json(self):
#         return {
#             "store_id": self.store_id,
#             "product_id": self.product_id,
#             "wholesale_price": self.wholesale_price,
#             "retail_price": self.retail_price,
#             "quantity": self.quantity
#         }
#     # FOr a given store,
#     # Get all items
#     # get a item with all vairations ashirvadh => ashirvadh atta, ashirvadh gulab jam, ashirvadh ..
    
#     @classmethod
#     def find_by_id(cls, _store_id):
#         """
#         Find all items of a given store id
#         """
#         return cls.query.filter_by(store_id=_store_id).all()

#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()

#     # @classmethod
#     # def find_by_id(cls, _id):
#     #     """
#     #     Find the given in the db
#     #     """
#     #     return cls.query.filter_by(id=_id).first()

#     # @classmethod
#     # def find_by_name(cls, name):
#     #     """
#     #     Find the given in the db
#     #     """
#     #     return cls.query.filter_by(name=name).first()

