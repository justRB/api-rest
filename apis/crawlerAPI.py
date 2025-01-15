from flask_restx import Namespace, Resource, fields
from config.config import authorizations
from decorators.authentication import auth_required
from services.services import crawler
from flask import request

api = Namespace("Crawler", "Get informations about a user", authorizations=authorizations)

crawler_input = api.model(
    "crawler_input", {
        "firstname": fields.String(min_length=1, required=True, default="kevin"),
        "lastname": fields.String(min_length=1, required=True, default="niel")
    }
)

crawler_output = api.model(
    "crawler_output", {
        "message": fields.String(description="Message")
    }
)

class CrawlerAPI(Resource):
    @auth_required
    @api.doc(security="apikey", body=crawler_input)
    @api.response(200, "Success research", crawler_output)
    @api.response(404, "Not found")
    def post(current_user, *args, **kwargs):
        result = crawler(request.get_json(), current_user)
        return result["output"], result["status"]
    
api.add_resource(CrawlerAPI, "")