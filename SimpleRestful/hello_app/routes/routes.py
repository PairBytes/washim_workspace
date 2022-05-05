from hello_app import api

from hello_app.controllers.hello_test import *

api.add_resource(HelloTest,"/")
api.add_resource(BooksView, '/books')
api.add_resource(BookView,'/books/<string:name>')
