from email.headerregistry import Address
from unicodedata import name
from flask_restful import Resource, reqparse
from hello_app import app
from hello_app.services.book_view_service import BookService


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
 
    def get(self,name):
        return BookService.get_book(name)

 
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str, help="Name can't be blank", required=True)
            parser.add_argument("address", type=str, help="Name can't be blank", required=True)
            parser.add_argument("name", type=str, help="Name can't be blank", required=True)
            parser.add_argument("name", type=str, help="Name can't be blank", required=True)
            args = parser.parse_args()

            return BookService.update_book(args[name],args[address])
        except Exception as e:
            return {"error": "something went wrong!"}
        
 
    def delete(self,name):
        return BookService.delete_book(name)