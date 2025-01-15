from flask_restx import Namespace, Resource, fields
from config.config import authorizations

api = Namespace("Easter egg", "A confidential secret")

class EasterEggAPI(Resource):
    def get(self):
        return {"message": "https://pointerpointer.com/"}
    
api.add_resource(EasterEggAPI, "")