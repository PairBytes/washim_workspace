from urllib import request
from flask_restful import Resource, reqparse
from hello_app import app
from hello_app.models.Books import BookModel
from hello_app.services.hello_service import HelloService


class HelloTest(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            args = parser.parse_args()
            print('argument: ',args["username"])
            return HelloService.get_username(args["username"])

        except Exception as e:
            app.logger.error("HelloTest:get:error:{}".format(str(e)))
    
class BooksView(Resource):
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help = "Can't leave blank"
    )
    parser.add_argument('price',
        type=float,
        required=True,
        help = "Can't leave blank"
    )
    parser.add_argument('author',
        type=str,
        required=True,
        help = "Can't leave blank"
    )'''
    def get(self):
        books = BookModel.query.all()
        return {'Books':list(x.json() for x in books)}
    
    def post(self):
        data = request.get_json()
        new_book = BookModel(data['name'],data['price'],data['author'])
        db.session.add(new_book)
        db.session.commit()
        return new_book.json(),201

class BookView(Resource):
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help = "Can't leave blank"
        )
    parser.add_argument('author',
        type=str,
        required=True,
        help = "Can't leave blank"
        )'''
    def get(self, name):
        book = BookModel.query.filter_by(name=name).first()
        if book:
            return book.json()
        return {'Message':'book not found'},404
    def put(self,name):
        data = request.get_json()
        book = BookModel.query.filter_by(name=name).first()

        if book:
            book.price = data["price"]
            book.author = data["author"]
        else:
            book = BookModel(name=name, **data)

        db.session.add(book)
        db.session.commit()

        return book.json()
    def delete(self,name):
        book = BookModel.query.filter_by(name=name).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'Message':'Deleted'}
        else:
            return {'Message':'Book not Found'},404