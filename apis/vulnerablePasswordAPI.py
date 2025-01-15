from flask_restx import Namespace, Resource, fields
from services.services import password_exist
from flask import request
from decorators.authentication import auth_required
from config.config import authorizations

api = Namespace('Vulnerable password', 'Check if password match with a list of vulnerables passwords', authorizations=authorizations)

input_model = api.model(
    "vulnerablePassword_input", {
        "password": fields.String(min_length=1, max_length=1000, required=True, description="Password to check")
    }
)

message_model = api.model(
    "vulnerablePassword_output", {
        "message": fields.String(description="Message")
    }
)

class VulnerablePasswordAPI(Resource):
    @auth_required
    @api.doc(security='apikey', body=input_model)
    @api.expect(input_model, validate=True)
    @api.response(200, 'Password match / Password doesn\'t match', message_model)
    @api.response(400, 'Validation error')
    def post(current_user, *args, **kwargs):
        result = password_exist(request.get_json(), current_user)
        return result["output"], result["status"]
    
api.add_resource(VulnerablePasswordAPI, "")
