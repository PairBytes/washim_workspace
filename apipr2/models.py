from cgi import print_exception
from unicodedata import name
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class BookModel(db.Model):
    __tablename__='books'

    id = db.Column(db.Integer, primary_key=True)
    name=db.column(db.String(80))
    price=db.column(db.Integer())
    author = db.column(db.String(80))

    def __init__(self,name,price,author):
        self.name=name
        self.price=price
        self.author=author
    
    def json(self):
        return {"name":self.name, "price":self.price, "author":self.author}