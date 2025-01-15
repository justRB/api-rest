from flask_restx import Namespace, Resource, fields
from services.services import user_add, get_users
from flask import request
from decorators.authentication import auth_required
from decorators.authorities import admin_authority
from config.config import authorizations

api = Namespace('Users', 'Manage users', authorizations=authorizations)

user_get_model = api.model(
    "user_get", {
        "id": fields.Integer(description="Id"),
        "username": fields.String(description="Username"),
        "authority": fields.String(description="Authority"),
        "creation_date": fields.DateTime(description="Creation date")
    }
)

user_add_model = api.model(
    "user_add", {
        "username": fields.String(min_length=8, max_length=12, required=True, description="Set username"),
        "password": fields.String(min_length=12, max_length=32, required=True, description="Set password"),
        "authority": fields.String(required=True, description="Set authority (user, admin)")
    }
)

class UsersAPI(Resource):
    @auth_required
    @admin_authority
    @api.doc(security="apikey", body=user_add_model)
    @api.expect(user_add_model, validate=True)
    @api.response(201, 'User has beeen created', user_get_model)
    @api.response(400, 'Validation error')
    @api.response(409, 'Conflict')
    def post(current_user, *args, **kwargs):
        result = user_add(request.get_json(), current_user)
        return result["output"], result["status"]
    
    @auth_required
    @admin_authority
    @api.doc(security="apikey")
    @api.response(200, 'Success', user_get_model)
    def get(current_user, *args, **kwargs):
        result = get_users(current_user)
        return result["output"], result["status"]
    
api.add_resource(UsersAPI, "")