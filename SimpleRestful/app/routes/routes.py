from app import api 
from app.controllers.hello_controller import Hello


api.add_resource(Hello,'/hello')