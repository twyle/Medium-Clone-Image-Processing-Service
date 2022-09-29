from flask import Blueprint, request
from flasgger import swag_from
from .controller import (
    handle_update_user,
)

user = Blueprint("user", __name__)


@user.route("/", methods=["PUT"])
@swag_from("./docs/update_user.yml", endpoint="user.update_user", methods=["PUT"])
def update_user():
    """Update a User."""
    return handle_update_user(request.args.get("id"), request.form, request.files)
