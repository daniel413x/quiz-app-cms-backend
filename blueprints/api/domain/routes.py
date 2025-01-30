from flask import Blueprint, jsonify, request, make_response
from models.user import User
from models.domain import Domain
from extensions import db
from utils.decode_jwt import decode_jwt

domain_bp = Blueprint("domain_bp", __name__)


# get a specific domain
@domain_bp.route("/<id>", methods=["GET"])
def get_domain(id):
    try:
        auth0_id = decode_jwt(request).get("sub")
        user = User.query.filter_by(auth0_id=auth0_id).first()
        domain = Domain.query.filter_by(id=id).first_or_404()
        if domain.user_id != user.id:
            return make_response(
                jsonify({"message": "Domain mismatch"}),
                403
            )
        return make_response(jsonify(domain.json()), 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting domain", "error": str(e)}), 500
        )


# update a domain
@domain_bp.route("/<id>", methods=["PATCH"])
def update_domain(id):
    try:
        auth0_id = decode_jwt(request).get("sub")
        user = User.query.filter_by(auth0_id=auth0_id).first()
        domain = Domain.query.filter_by(id=id).first_or_404()
        if domain.user_id != user.id:
            return make_response(
                jsonify({"message": "Domain mismatch"}),
                403
            )
        if domain:
            data = request.get_json()
            domain.name = data["name"]
            domain.slug = data["slug"]
            domain.private = data["private"]
            db.session.commit()
            return make_response(jsonify({"message": "domain updated"}), 204)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error updating domain", "error": str(e)}), 500
        )


# delete a domain
@domain_bp.route("/<id>", methods=["DELETE"])
def delete_domain(id):
    try:
        domain = Domain.query.filter_by(id=id).first()
        if domain:
            db.session.delete(domain)
            db.session.commit()
            return make_response(jsonify({"message": "domain deleted"}), 204)
        return jsonify(make_response(jsonify({"message": "domain not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error deleting domain", "error": str(e)}), 500
        )
