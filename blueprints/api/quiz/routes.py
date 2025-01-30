from flask import Blueprint, jsonify, request, make_response
from models.quiz import Quiz
from extensions import db
from models.quiz_category import QuizCategory
from models.serializers.quiz_get_many_serializer import QuizGetManySerializer
from models.serializers.quiz_serializer import QuizSerializer
from models.user import User
from utils.decode_jwt import decode_jwt

quiz_bp = Blueprint("quiz_bp", __name__)


@quiz_bp.route("", methods=["POST"])
def create_quiz():
    try:
        auth0_id = decode_jwt(request).get("sub")
        user = User.query.filter_by(auth0_id=auth0_id).first()
        domain_id = user.domain.id
        data = request.get_json()
        quiz_slug = data["slug"]
        slug_not_unique = Quiz.query.join(QuizCategory).filter(
            Quiz.slug == quiz_slug,
            QuizCategory.domain_id == domain_id
        ).first()
        if slug_not_unique:
            return make_response(
                jsonify({"message": "Slug must be unique"}), 400
            )
        category_slug = data["categorySlug"]
        category = QuizCategory.query.filter_by(slug=category_slug).first_or_404()
        new_quiz = Quiz(name=data["name"], category_id=category.id, slug=quiz_slug)
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
        serializer = QuizGetManySerializer(many=True)
        quizzes = serializer.dump(quiz)
        return jsonify(quizzes, 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "Error getting quiz", "error": str(e)}), 500
        )


# get a specific quiz
@quiz_bp.route("/<category_slug>", methods=["GET"])
def get_quiz(category_slug):
    try:
        auth0_id = decode_jwt(request).get("sub")
        user = User.query.filter_by(auth0_id=auth0_id).first()
        category = QuizCategory.query.filter(QuizCategory.slug == category_slug).first_or_404()
        if category.domain.user_id != user.id:
            return make_response(
                jsonify({"message": "Domain mismatch"}),
                403
            )
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
@quiz_bp.route("/<category_slug>/<quiz_slug>", methods=["GET"])
def get_quiz_by_cat_name_quiz_name(category_slug, quiz_slug):
    try:
        auth0_id = decode_jwt(request).get("sub")
        user = User.query.filter_by(auth0_id=auth0_id).first()
        category = QuizCategory.query.filter(QuizCategory.slug == category_slug).first_or_404()
        if category.domain.user_id != user.id:
            return make_response(
                jsonify({"message": "Domain mismatch"}),
                403
            )
        category_id = category.id
        # check category_id to query within only the category/domain
        queried_quiz = Quiz.query.filter(Quiz.category_id == category_id, Quiz.slug == quiz_slug).first_or_404()
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
            quiz.slug = data["slug"]
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
