from flask_restx import Namespace, Resource, fields
from services.services import login
from flask import request

api = Namespace('Authentication', 'To be authenticate')

input_model = api.model(
    "authentication_input", {
        "username": fields.String(min_length=8, max_length=12, required=True, description="Username", default="kevin_niel"),
        "password": fields.String(min_length=12, max_length=32, required=True, description="Password", default="supermotdepasse")
    }
)

message_model = api.model(
    "authentication_output", {
        "message": fields.String()
    }
)

class AuthenticationAPI(Resource):
    @api.doc(body=input_model)
    @api.expect(input_model, validate=True)
    @api.response(200, 'User is authenticated', message_model)
    @api.response(400, 'Validation error')
    @api.response(401, 'Authentication fail', message_model)
    def post(self):
        result = login(request.get_json())
        return result["output"], result["status"]

api.add_resource(AuthenticationAPI, "")