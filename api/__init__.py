import orjson
import pendulum

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask.json import JSONEncoder
from loguru import logger

from jsonschema import ValidationError
from marshmallow import ValidationError as MarshmallowValidationError

from api.errors import APIError, APIErrorType, WrappedAPIError
from api.controllers import register_blueprints

from werkzeug.exceptions import NotFound

from api.constants import OPENAI_API_KEY
import openai

class FastJSONEncoder(JSONEncoder):
    def default(self, obj):
        return orjson.dumps(obj)
    
def before_request():
    """Before Request execute"""
    setattr(request, "start", pendulum.now("UTC"))
    logger.info(f"Request {request.method} received on {request.path}")
    
def _wrap_unknown_exceptions(error) -> APIError:
    code = error.code if hasattr(error, "code") else 500
    error_category = APIErrorType.CRITICAL if code >= 500 else APIErrorType.BUSINESS
    message = (
        error.message
        if hasattr(error, "message")
        else error.description
        if hasattr(error, "description")
        else str(error)
    )
    error_type = type(error)
    if error_type == NotImplementedError:
        code = 501
        message = "Not yet implemented"
    elif error_type in (ValidationError, MarshmallowValidationError):
        code = 400
        error_category = APIErrorType.BUSINESS
        message = str(error)
    elif error_type == NotFound:
        code = 404
        error_category = APIErrorType.BUSINESS
        message = str(error)
    else:
        logger.error(f"Unmapped Exception {error_type}", details=str(error))

    return WrappedAPIError(cause=error, code=code, message=message, error_type=error_category)
    
def exception_handler(error):
    if not isinstance(error, APIError):
        error = _wrap_unknown_exceptions(error)

    response_body = {"type": "ERROR", "message": error.message}

    if error.payload:
        response_body["payload"] = error.payload

    if error.code == 404:
        logger.info(error.message)
    else:
        logger.exception(error.message)

    return jsonify(response_body), error.code

def create_api():
    app = Flask(__name__)
    
    app.json_encoder = FastJSONEncoder
    app.url_map.strict_slashes = False
    
    openai.api_key = OPENAI_API_KEY
    
    register_blueprints(app)
    
    app.register_error_handler(Exception, exception_handler)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    app.before_request(before_request)
    
    return app