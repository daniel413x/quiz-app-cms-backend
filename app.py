from flask import Flask
from flask_cors import CORS
from os import environ

from blueprints.api.quiz_answer.routes import quiz_answer_bp
from blueprints.api.quiz_category.routes import quiz_category_bp
from blueprints.api.quiz.routes import quiz_bp
from blueprints.api.quiz_question.routes import quiz_question_bp
from blueprints.test.routes import test_bp
from extensions import db
from consts.routes import API_ROUTE, TEST_ROUTE, QUIZ_ROUTE, QUIZ_CATEGORY_ROUTE, QUIZ_QUESTION_ROUTE, QUIZ_ANSWER_ROUTE

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
        }
    },
)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL")

db.init_app(app)

with app.app_context():
    db.create_all()

# note that these prefixers are for eliminating redundancy of defining this string route down the line in the blueprints.api.users.routes file. as long as the line below is present, you can define those routes as "/" "/<id>" etc
# app.register_blueprint(quiz_bp, url_prefix=f"/{API_ROUTE}/{QUIZ_ROUTE}")
app.register_blueprint(quiz_category_bp, url_prefix=f"/{API_ROUTE}/{QUIZ_CATEGORY_ROUTE}")
app.register_blueprint(quiz_question_bp, url_prefix=f"/{API_ROUTE}/{QUIZ_QUESTION_ROUTE}")
app.register_blueprint(quiz_answer_bp, url_prefix=f"/{API_ROUTE}/{QUIZ_ANSWER_ROUTE}")
app.register_blueprint(quiz_bp, url_prefix=f"/{API_ROUTE}/{QUIZ_ROUTE}")
app.register_blueprint(test_bp, url_prefix=f"/{API_ROUTE}/{TEST_ROUTE}")


@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized.")
