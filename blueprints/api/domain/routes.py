from flask import Blueprint, jsonify, request, make_response
from models.user import User
from models.domain import Domain
from extensions import db
import coolname

domain_bp = Blueprint("domain_bp", __name__)


# get a specific domain
@domain_bp.route("/by-auth0-id/<id>", methods=["GET"])
def get_domain(id):
    try:
        user = User.query.filter_by(auth0_id=id).first()
        print(user)
        print(user)
        print(user)
        domain = Domain.query.filter_by(user_id=user.id).first()
        if domain:
            return make_response(jsonify({"domain": domain.json()}), 200)
        return jsonify(make_response(jsonify({"message": "domain not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting domain", "error": str(e)}), 500
        )


# update a domain
@domain_bp.route("/<id>", methods=["PUT"])
def update_domain(id):
    try:
        domain = Domain.query.filter_by(id=id).first()
        if domain:
            data = request.get_json()
            domain.name = data["name"]
            db.session.commit()
            return make_response(jsonify({"message": "domain updated"}), 204)
        return jsonify(make_response(jsonify({"message": "domain not found"})), 404)
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
