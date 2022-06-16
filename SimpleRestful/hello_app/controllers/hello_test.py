from unicodedata import name
import urllib.request
from flask_restful import Resource, reqparse
from hello_app import app
from hello_app.models.Books import BookModel, db
from hello_app.services.hello_service import HelloService
from hello_app.services.book_view_service import BookService
from flask import request

# from hello_app.__init__ import token_required
from hello_app.controllers.decorators.authenticated import authenticated

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
    
    # @token_required
    @authenticated()
    def get(self):
        
        books = BookModel.query.all()
        return {'Books':list(x.json() for x in books)}
        
 
    def post(self):
        data = request.get_json()
        #data = BooksView.parser.parse_args()
 
        new_book = BookModel(data['name'],data['price'],data['author'])
        db.session.add(new_book)
        db.session.commit()
        return new_book.json(),201
 
 
class BookView(Resource):
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help = "Can't leave blank")
    parser.add_argument('author', type=str,  required=True, help = "Can't leave blank")'''
 
    def get(self,name):
        return BookService.get_book(name)

 
    def put(self,name):
        # try:
        #     parser = reqparse.RequestParser()
        #     parser.add_argumetn('name', type=float, required=True, help = "Can't leave blank")
        #     parser.add_argument('price', type=float, required=True, help = "Can't leave blank")
        #     parser.add_argument('author', type=str,  required=True, help = "Can't leave blank")
        #     args = parser.parse_args()
        #     return BookService.update_book(args['name'],args['price'],args['author'])
        # except Exception as e:
        #     return {"error": "something went wrong!"}
        return BookService.put_book(name)
        
 
    def delete(self,name):
        return BookService.delete_book(name)