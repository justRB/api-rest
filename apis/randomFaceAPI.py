from flask_restx import Namespace, Resource, fields
from config.config import authorizations
from decorators.authentication import auth_required
from services.services import random_face

api = Namespace('Random face', "Generate a random face who doesn't exist", authorizations=authorizations)

randomFace_output = api.model(
    "randomFace_output", {
        "message": fields.String(description="Message")
    }
)

class RandomFaceAPI(Resource):
    @auth_required
    @api.doc(security='apikey')
    @api.response(201, 'Random face has been generated', randomFace_output)
    @api.response(500, "Error")
    def get(current_user, *args, **kwargs):
        result = random_face(current_user)
        return result["output"], result["status"]
    
api.add_resource(RandomFaceAPI, "")