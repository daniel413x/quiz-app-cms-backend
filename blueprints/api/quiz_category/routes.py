from flask import Blueprint, jsonify, request, make_response
from models.quiz_category import QuizCategory
from models.user import User
from extensions import db
from models.serializers.quiz_category_get_many_serializer import QuizCategoryGetManySerializer
from utils.decode_jwt import decode_jwt

quiz_category_bp = Blueprint("quiz_category_bp", __name__)


@quiz_category_bp.route("", methods=["POST"])
def create_quiz_category():
    try:
        auth0_id = decode_jwt(request).get("sub")
        user = User.query.filter_by(auth0_id=auth0_id).first()
        domain_id = user.domain.id
        data = request.get_json()
        slug_not_unique = QuizCategory.query.filter_by(slug=data["slug"], domain_id=domain_id).first()
        if slug_not_unique:
            return make_response(
                jsonify({"message": "Slug must be unique"}), 400
            )
        new_quiz_category = QuizCategory(name=data["name"], slug=data["slug"], domain_id=user.domain.id)
        db.session.add(new_quiz_category)
        db.session.commit()
        return jsonify({}, 201)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error creating quiz_category", "error": str(e)}), 500
        )


@quiz_category_bp.route("", methods=["GET"])
def get_quiz_categories():
    try:
        auth0_id = decode_jwt(request).get("sub")
        user = User.query.filter_by(auth0_id=auth0_id).first()
        quiz_category = QuizCategory.query.filter_by(domain_id=user.domain.id)
        serializer = QuizCategoryGetManySerializer(many=True)
        quizzes = serializer.dump(quiz_category)
        return jsonify(quizzes, 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quiz_category", "error": str(e)}), 500
        )


# update a quiz_category
@quiz_category_bp.route("/<id>", methods=["PUT"])
def update_quiz_category(id):
    try:
        auth0_id = decode_jwt(request).get("sub")
        user = User.query.filter_by(auth0_id=auth0_id).first()
        quiz_category = QuizCategory.query.filter_by(id=id).first()
        if quiz_category:
            if quiz_category.domain.id != user.domain.id:
                return make_response(
                    jsonify({"message": "Domain mismatch"}),
                    403
                )
            data = request.get_json()
            slug_not_unique = QuizCategory.query.filter_by(slug=data["slug"]).first()
            if slug_not_unique:
                return make_response(
                    jsonify({"message": "Slug must be unique"}), 400
                )
            quiz_category.name = data["name"]
            db.session.commit()
            return make_response(jsonify({"message": "quiz_category updated"}), 204)
        return jsonify(make_response(jsonify({"message": "quiz_category not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error updating quiz_category", "error": str(e)}), 500
        )


# delete a quiz_category
@quiz_category_bp.route("/<id>", methods=["DELETE"])
def delete_quiz_category(id):
    try:
        auth0_id = decode_jwt(request).get("sub")
        user = User.query.filter_by(auth0_id=auth0_id).first()
        quiz_category = QuizCategory.query.filter_by(id=id).first()
        if quiz_category:
            if quiz_category.domain.id != user.domain.id:
                return make_response(
                    jsonify({"message": "Domain mismatch"}),
                    403
                )
            db.session.delete(quiz_category)
            db.session.commit()
            return make_response(jsonify({"message": "quiz_category deleted"}), 204)
        return jsonify(make_response(jsonify({"message": "quiz_category not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error deleting quiz_category", "error": str(e)}), 500
        )
