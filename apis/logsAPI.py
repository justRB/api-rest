from flask_restx import Namespace, Resource, fields
from services.services import get_logs
from decorators.authentication import auth_required
from decorators.authorities import admin_authority
from config.config import authorizations

api = Namespace('Logs', 'Consult logs', authorizations=authorizations)

log_get_model = api.model(
    "log_get", {
        "id": fields.Integer(description="Id"),
        "date": fields.DateTime(description="Date"),
        "username": fields.String(description="Username"),
        "description": fields.String(description="Description")
    }
)

class LogsAPI(Resource):
    @auth_required
    @admin_authority
    @api.doc(security="apikey")
    @api.response(200, 'Success', log_get_model)
    def get(current_user, *args, **kwargs):
        result = get_logs(current_user)
        return result["output"], result["status"]
    
api.add_resource(LogsAPI, "")