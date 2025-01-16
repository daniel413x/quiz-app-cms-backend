from flask import Blueprint, jsonify, request, make_response
from models.quiz import Quiz
from models.quiz_question import QuizQuestion
from extensions import db
from models.serializers.quiz_question_serializer import QuizQuestionSerializer
from marshmallow import ValidationError

quiz_question_bp = Blueprint("quiz_question_bp", __name__)

@quiz_question_bp.route("", methods=["POST"])
def create_quiz():
    try:
        data = request.get_json()
        quiz_question_schema = QuizQuestionSerializer()
        answers = data.get("answers", [])
        quiz_name = data.get("quizName")
        quiz = Quiz.query.filter(Quiz.name.ilike(quiz_name)).first_or_404()
        question_data = {
            "question": data["question"],
            "answers": answers  # Add the deserialized answers to the question
        }
        print(question_data)
        new_quiz_question = quiz_question_schema.load(question_data)
        new_quiz_question.quiz_id = quiz.id
        db.session.add(new_quiz_question)
        db.session.commit()
        result = quiz_question_schema.dump(new_quiz_question)
        return jsonify(result), 201

    except ValidationError as e:
        # Handle validation errors
        return make_response(jsonify({"message": "Validation error", "errors": e.messages}), 400)

    except Exception as e:
        # Handle other exceptions
        return make_response(
            jsonify({"message": "Error creating quiz", "error": str(e)}), 500
        )


# get all quizzes
@quiz_question_bp.route("/", methods=["GET"])
def get_quizzes():
    try:
        quiz = Quiz.query.all()
        quiz_data = [
            {
                "id": quiz.id,
                "name": quiz.name,
                "email": quiz.email,
            }
            for quiz in quiz
        ]
        return jsonify(quiz_data, 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quiz", "error": str(e)}), 500
        )


# get a specific quiz
@quiz_question_bp.route("/<id>", methods=["GET"])
def get_quiz(id):
    try:
        query = QuizQuestion.query.filter_by(id=id).first()
        quiz = QuizQuestionSerializer().dump(query)

        if quiz:
            return make_response(jsonify(quiz), 200)
        return jsonify(make_response(jsonify({"message": "quiz not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quiz", "error": str(e)}), 500
        )


# update a quiz
@quiz_question_bp.route("/<id>/", methods=["PUT"])
def update_quiz(id):
    try:
        quiz = Quiz.query.filter_by(id=id).first()
        if quiz:
            data = request.get_json()
            quiz.name = data["name"]
            quiz.email = data["email"]
            db.session.commit()
            return make_response(jsonify({"message": "quiz updated"}), 200)
        return jsonify(make_response(jsonify({"message": "quiz not found"})), 404)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error updating quiz", "error": str(e)}), 500
        )


# delete a quiz
@quiz_question_bp.route("/<id>/", methods=["DELETE"])
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
