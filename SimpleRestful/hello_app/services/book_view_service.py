from flask_restful import Resource
from hello_app.models.Books import BookModel, db
# from hello_app.__init__ import token_required

class BookService(Resource):
    # to get individual data request 
    # Like 
    # http://localhost:5000/books/book1, /books/<string:name>
    # @token_required
    def get_book(name):
        # try:
        book = BookModel.query.filter_by(name=name).first()
        # print("Name:",name)
        if book:
            return book.json()
        
        return {'message':'book not found'},404
    # except Exception as e:
        #      return {"error": "something went wrong!"}
    
    # To Put/Edit/Update data 
    def put_book(name):
        data = request.get_json()
        #data = BookView.parser.parse_args()
 
        book = BookModel.query.filter_by(name=name).first()
 
        if book:
            book.price = data["price"]
            book.author = data["author"]
        else:
            book = BookModel(name=name,**data)
 
        # db.session.add(book)
        # db.session.commit()
        return book.json()

    def delete_book(name):
        book = BookModel.query.filter_by(name=name).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message': 'book not found'},404

