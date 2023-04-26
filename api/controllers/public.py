from flask import Blueprint, jsonify
from loguru import logger

from api.constants import CODE_COMMIT, DEPLOYED_AT, VERSION, ENVIRONMENT

from pathlib import Path

public_bp = Blueprint("public", __name__)


@public_bp.route("/", endpoint="root")
def version():    
    content = {
        "environment": ENVIRONMENT,
        "version": VERSION,
        "commit": CODE_COMMIT,
        "deployed_at": DEPLOYED_AT,
    }

    return jsonify(content), 200