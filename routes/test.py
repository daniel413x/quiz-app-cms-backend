import app
from flask import Blueprint, jsonify
from consts.routes import TEST_ROUTE

test_bp = Blueprint(TEST_ROUTE, __name__, template_folder="templates")


@test_bp.route(f"{TEST_ROUTE}", methods=["GET"])
def test():
    return jsonify({"message": "The server is running"})
