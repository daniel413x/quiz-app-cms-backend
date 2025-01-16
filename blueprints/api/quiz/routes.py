from flask import Blueprint, jsonify, request, make_response
from models.quiz import Quiz
from extensions import db
from models.quiz_category import QuizCategory
from models.serializers.quiz_get_many_serializer import QuizGetManySerializer
from models.serializers.quiz_serializer import QuizSerializer

quiz_bp = Blueprint("quiz_bp", __name__)


@quiz_bp.route("", methods=["POST"])
def create_quiz():
    try:
        data = request.get_json()
        category_name = data["categoryName"]
        category = QuizCategory.query.first_or_404(category_name)
        new_quiz = Quiz(name=data["name"], category_id=category.id)
        db.session.add(new_quiz)
        db.session.commit()
        return jsonify(
            {}
        )
    except Exception as e:
        return make_response(
            jsonify({"message": "Error creating quiz", "error": str(e)}), 500
        )


# get all quizzes
@quiz_bp.route("/", methods=["GET"])
def get_quizzes():
    try:
        quiz = Quiz.query.all()
        quiz_data = [
            {
                "id": quiz.id,
                "name": quiz.name,
            }
            for quiz in quiz
        ]
        return jsonify(quiz_data, 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quiz", "error": str(e)}), 500
        )


# get a specific quiz
@quiz_bp.route("/<category_name>", methods=["GET"])
def get_quiz(category_name):
    try:
        category = QuizCategory.query.filter(QuizCategory.name.ilike(category_name)).first_or_404()
        category_id = category.id
        serializer = QuizGetManySerializer(many=True)
        quizzes_by_cat_id = Quiz.query.filter_by(category_id=category_id)
        quizzes = serializer.dump(quizzes_by_cat_id)
        return jsonify(quizzes, 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quizzes by category name", "error": str(e)}), 500
        )


# get a quiz that belongs to a category
@quiz_bp.route("/<category_name>/<quiz_name>", methods=["GET"])
def get_quiz_by_cat_name_quiz_name(category_name, quiz_name):
    try:
        category = QuizCategory.query.filter(QuizCategory.name.ilike(category_name)).first_or_404()
        category_id = category.id
        queried_quiz = Quiz.query.filter(Quiz.category_id == category_id, Quiz.name.ilike(quiz_name)).first_or_404()
        serializer = QuizSerializer()
        quiz = serializer.dump(queried_quiz)
        return jsonify(quiz, 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quizzes by category name", "error": str(e)}), 500
        )


# update a quiz
@quiz_bp.route("/<id>", methods=["PUT"])
def update_quiz(id):
    try:
        quiz = Quiz.query.filter_by(id=id).first()
        if quiz:
            data = request.get_json()
            quiz.name = data["name"]
            db.session.commit()
            return make_response(jsonify({"message": "quiz updated"}), 204)
        return jsonify(make_response(jsonify({"message": "quiz not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error updating quiz", "error": str(e)}), 500
        )


# delete a quiz
@quiz_bp.route("/<id>/", methods=["DELETE"])
def delete_quiz(id):
    try:
        quiz = Quiz.query.filter_by(id=id).first()
        if quiz:
            db.session.delete(quiz)
            db.session.commit()
            return make_response(jsonify({"message": "quiz deleted"}), 200)
        return jsonify(make_response(jsonify({"message": "quiz not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error deleting quiz", "error": str(e)}), 500
        )
