from hello_app import api

from hello_app.controllers.hello_test import HelloTest

api.add_resource(HelloTest,"/hello")

