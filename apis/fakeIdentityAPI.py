from flask_restx import Namespace, Resource, fields
from services.services import fake_identity
from decorators.authentication import auth_required
from config.config import authorizations

api = Namespace('Fake identity', 'Generate a fake identity', authorizations=authorizations)

fake_identity_get_model = api.model(
    "fakeIdentity_get", {
        "name": fields.String(description="Name"),
        "address": fields.String(description="Address"),
        "email": fields.String(description="Email"),
        "birthdate": fields.String(description="Birthdate")
    }
)

class FakeIdentityAPI(Resource):
    @auth_required
    @api.doc(security="apikey")
    @api.response(201, 'Identity has been generated', fake_identity_get_model)
    def get(current_user, *args, **kwargs):
        result = fake_identity(current_user)
        return result["output"], result["status"]
    
api.add_resource(FakeIdentityAPI, "")