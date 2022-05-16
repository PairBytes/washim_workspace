from hello_app import db

class BookModel(db.Model):
    __tablename__= 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Integer())
    author = db.Column(db.String(80))

    def __init__(self, name, price, author):
        self.name = name
        self.price = price
        self.author = author

    def json(self):
        return {"Name":self.name, "Price":self.price, "Author":self.author}
    
    def save(self):
        db.session.add()
        db.session.commit()
    
    def delete(self):
        db.session.delete()
        db.session.commit()
