from . import db

# PRODUCT DETAIL TABLE
class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default = 'default.jpg')
    book_detail = db.relationship("BookDetail", backref="categories", cascade='all, delete-orphan')

class BookDetail(db.Model):
    __tablename__ = 'book_detail'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default = 'default.jpg')
    price = db.Column(db.Float)
    book_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return f"ID: {self.id}\nName: {self.name}\nDescription: {self.description}"

orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('book_id',db.Integer,db.ForeignKey('book_detail.id'),nullable=False),
    db.PrimaryKeyConstraint('order_id', 'book_id') )

# ORDER TABLE
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    total_cost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    item_detail = db.relationship("BookDetail", secondary='orderdetails', backref="orders")
