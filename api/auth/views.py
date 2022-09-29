from flask import Blueprint, jsonify, request
from flasgger import swag_from
from .controller import (
    handle_create_user,
)

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
@swag_from("./docs/register_user.yml", endpoint="auth.register", methods=["POST"])
def register():
    """Create a new User."""
    return handle_create_user(request.form, request.files)
