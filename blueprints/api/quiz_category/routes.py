from flask import Blueprint, jsonify, request, make_response
from models.quiz_category import QuizCategory
from extensions import db
from models.serializers.quiz_category_get_many_serializer import QuizCategoryGetManySerializer

quiz_category_bp = Blueprint("quiz_category_bp", __name__)


@quiz_category_bp.route("", methods=["POST"])
def create_quiz_category():
    try:
        data = request.get_json()
        new_quiz_category = QuizCategory(name=data["name"])
        db.session.add(new_quiz_category)
        db.session.commit()
        return jsonify(
            {
                "id": new_quiz_category.id,
                "name": new_quiz_category.name,
            }
        )
    except Exception as e:
        return make_response(
            jsonify({"message": "Error creating quiz_category", "error": str(e)}), 500
        )


# get all quiz_categories
@quiz_category_bp.route("", methods=["GET"])
def get_quiz_categories():
    try:
        quiz_category = QuizCategory.query.all()
        serializer = QuizCategoryGetManySerializer(many=True)
        quizzes = serializer.dump(quiz_category)
        print(quiz_category)
        return jsonify(quizzes, 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quiz_category", "error": str(e)}), 500
        )


# get a specific quiz_category
@quiz_category_bp.route("/<id>/", methods=["GET"])
def get_quiz_category(id):
    try:
        quiz_category = QuizCategory.query.filter_by(id=id).first()
        if quiz_category:
            return make_response(jsonify({"quiz_category": quiz_category.json()}), 200)
        return jsonify(make_response(jsonify({"message": "quiz_category not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quiz_category", "error": str(e)}), 500
        )


# update a quiz_category
@quiz_category_bp.route("/<id>", methods=["PUT"])
def update_quiz_category(id):
    try:
        quiz_category = QuizCategory.query.filter_by(id=id).first()
        if quiz_category:
            data = request.get_json()
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
        quiz_category = QuizCategory.query.filter_by(id=id).first()
        if quiz_category:
            db.session.delete(quiz_category)
            db.session.commit()
            return make_response(jsonify({"message": "quiz_category deleted"}), 204)
        return jsonify(make_response(jsonify({"message": "quiz_category not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error deleting quiz_category", "error": str(e)}), 500
        )
