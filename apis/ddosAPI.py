from flask_restx import Namespace, Resource, fields
from services.services import ddos
from decorators.authentication import auth_required
from decorators.authorities import admin_authority
from config.config import authorizations
from flask import request

api = Namespace('DDOS', 'If you want FBI open the door, start the process, that is your problem', authorizations=authorizations)

input_model = api.model(
    "ddos_post", {
        "domain_name": fields.String(required=True, description="Domain to target (example : kevinniel.fr)", default="kevinniel.fr"),
        "port": fields.Integer(min=0, max=65535, required=True, description="Port (example : 80)", default=443),
        "time_execution": fields.Integer(min=5, max=30, required=True, description="Time execution", default=5)
    }
)

class DdosAPI(Resource):
    @auth_required
    @admin_authority
    @api.doc(security="apikey", body=input_model)
    @api.expect(input_model, validate=True)
    @api.response(200, 'Ddos success')
    @api.response(400, 'Fail')
    def post(current_user, *args, **kwargs):
        result = ddos(request.get_json(), current_user)
        return result["output"], result["status"]
    
api.add_resource(DdosAPI, "")