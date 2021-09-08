from db import db

# from models.secondary_tables import products_bill
from utils import date_format


class ProductModel(db.Model):
    """
    Product Class, Behaves like a Record in db.

    This class is in relationship with StoreModel
    """

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(300))
    description = db.Column(db.String(500))
    category = db.Column(db.String(40), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    # these created on and updated_on are causing error in heroku, posstgresql
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    # column names, i.e, actual_price, wholesale_price, retail_price if changed. Update them in configs.constants
    actual_price = db.Column(db.Float(precision=3), nullable=False)
    wholesale_price = db.Column(db.Float(precision=3), nullable=False)
    retail_price = db.Column(db.Float(precision=3), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    barcode = db.Column(db.String)
    brand = db.Column(db.String(100))
    enable = db.Column(db.Boolean(), server_default='True')
    # store -> reference from StoreModel

    # bills_in = db.relationship('CustomerOrderModel', secondary=products_bill, back_populates="products")
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
    # price = db.Column(db.Float(precision=2))
    # price = db.Column(db.Float(precision=2))

    def __init__(self, name, url, category, description, unit, actual_price, wholesale_price, retail_price, quantity, brand, barcode):
        self.name = name
        self.url = url
        self.category = category
        self.description = description
        self.unit = unit
        self.actual_price = actual_price
        self.wholesale_price = wholesale_price
        self.retail_price = retail_price
        self.quantity = quantity
        self.brand = brand
        self.barcode = barcode

    def json(self):
        return {
            "id": self.id,
            "barcode": self.barcode,
            "name": self.name,
            "url": self.url,
            "category": self.category,
            "description": self.description,
            "brand": self.brand,
            "unit": self.unit,
            "actual_price": self.actual_price,
            "wholesale_price": self.wholesale_price,
            "retail_price": self.retail_price,
            "quantity": self.quantity,
            "created_on": date_format(self.created_on),
            "updated_on": date_format(self.updated_on),
            "enable": self.enable,
        }

    def order_json(self):
        return {
            "id": self.id,
            "barcode": self.barcode,
            "name": self.name,
            "url": self.url,
            "category": self.category,
            "unit": self.unit,
        }

    @classmethod
    def _base_query(cls, _uid, _sid):
        """
        Base query for Product Model class, to make sure we search in only in user allowed stores.
        """
        return cls.query.filter(cls.store.any(user_id=_uid, id=_sid))

    @classmethod
    def find_similar(cls, _uid, _sid, name):
        """
        Find the given in the db
        """
        # query = meta.Session.query(User).filter_by(
        #     firstname.like(search_var1),
        #     lastname.like(search_var2)
        #     )
        # cls.query.filter(cls.name.like("%" + name + "%")).all()
        # TODO - one can use contains
        # .filter(cls.name.like(name)).all()
        return cls._base_query(_uid, _sid).filter(cls.name.like("%" + name + "%")).all()

    @classmethod
    def find_by_id(cls, _uid, _sid, _pid):
        """
        Find the given product id, in the db
        """
        return cls._base_query(_uid, _sid).filter_by(id=_pid).scalar()

    @classmethod
    def find_in_user_store_by_barcode_or_id(cls, _uid, _sid, _id_or_barcode):
        """
        Find the given product id, in the db
        """
        return cls._base_query(_uid, _sid).filter(db.or_(cls.id == _id_or_barcode, cls.barcode == str(_id_or_barcode))).scalar()

    @classmethod
    def find_in_user_store(cls, _uid, _sid, _pid):
        """
        Find the product from a particular user store
        """
        # cls.query.filter(cls.store.any(id=_sid)).filter(cls.id == _pid).first()
        return cls._base_query(_uid, _sid).filter_by(id=_pid).scalar()

    @classmethod
    def find_by_name(cls, _uid, _sid, name):
        """
        Find the given in the db
        """
        return cls._base_query(_uid, _sid).filter_by(name=name).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
