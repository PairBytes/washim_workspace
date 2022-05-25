from hello_app import api

from hello_app.controllers.hello_test import *
from hello_app.Token.Token_Create import login


api.add_resource(HelloTest,"/")
api.add_resource(BooksView, '/books')
api.add_resource(BookView,'/books/<string:name>')
app.add_url_rule(login, '/login')  