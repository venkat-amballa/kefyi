from db import db
from models.secondary_tables import products_bill

class ProductModel(db.Model):
    """
    Product Class, Behaves like a Record in db.

    This class is in relationship with StoreModel
    """

    __tablename__ = "products"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # description = db.Column(db.String(500))
    category = db.Column(db.String(40), nullable=False)
    # these created on and updated_on are causing error in heroku, posstgresql
    # created_on = db.Column(db.DateTime, server_default=db.func.now())
    # updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    # column names, i.e, actual_price, wholesale_price, retail_price if changed. Update them in constants.py
    actual_price = db.Column(db.Float(precision=3), nullable=False)
    wholesale_price = db.Column(db.Float(precision=3), nullable=False)
    retail_price = db.Column(db.Float(precision=3), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    bills_in = db.relationship('CustomerBill', secondary=products_bill, back_populates="products")
    # brand_name = 
    # create_by = 
    # created_at = 
    # updated_by = 
    # updated_at = 
    # public = 
    # manufactured_on = db.dColumn(db.DateTime, nullable=False)
    # expiries_on = db.Column(db.DateTime, nullable=False)
    # imported_on 

    # store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    # Ashirvadh_Aata_100g
    # brand
    # category (Food, Snacks, Diary, Electronics, Clothing, .... etc)
    # description
    # price = db.Column(db.Float(precision=2))
    # price = db.Column(db.Float(precision=2))

    def __init__(self, name, category, actual_price, wholesale_price, retail_price, quantity):
        self.name = name
        self.category = category
        self.actual_price = actual_price
        self.wholesale_price = wholesale_price
        self.retail_price = retail_price
        self.quantity = quantity

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "category":self.category,
            "actual_price": self.actual_price,
            "wholesale_price": self.wholesale_price,
            "retail_price": self.retail_price,
            "quantity": self.quantity
        }

    @classmethod
    def find_all(cls):
        """
        Find the given in the db
        """
        return cls.query.all()

    @classmethod
    def find_similar(cls, name):
        """
        Find the given in the db
        """
        # query = meta.Session.query(User).filter_by(
        #     firstname.like(search_var1),
        #     lastname.like(search_var2)
        #     )
        return cls.query.filter(cls.name.like("%" + name + "%"))

    @classmethod
    def find_by_id(cls, _id):
        """
        Find the given in the db
        """
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        """
        Find the given in the db
        """
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
