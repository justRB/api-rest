from flask_restx import Namespace, Resource, fields
from config.config import authorizations
from decorators.authentication import auth_required
from services.services import isValidEmail
from flask import request

api = Namespace("Is valid email", "Check is the email exist", authorizations=authorizations)

isValidEmail_input = api.model(
    "isValidEmail_input", {
        "email": fields.String(min_length=1, required=True)
    }
)

isValidEmail_output = api.model(
    "isValidEmail_output", {
        "email": fields.String(min_length=1, required=True)
    }
)

class IsValidEmailAPI(Resource):
    @auth_required
    @api.doc(security="apikey", body=isValidEmail_input)
    @api.response(200, "Email is valid")
    @api.response(404, "Email is invalid")
    def post (current_user, *args, **kwargs):
        result = isValidEmail(request.get_json(), current_user)
        return result["output"], result["status"]
    
api.add_resource(IsValidEmailAPI, "")