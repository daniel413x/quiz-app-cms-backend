import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID


class QuizAnswer(db.Model):
    __tablename__ = "quiz_answer"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    correct_answer = db.Column(db.Boolean, nullable=False)

    order = db.Column(db.Integer, nullable=True)

    # Foreign key to QuizQuestion
    quiz_question_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quiz_question.id'), nullable=False)

    # Relationship to question
    question = db.relationship('QuizQuestion', back_populates='answers')

    def json(self):
        return {
            "id": str(self.id),
            "answer": self.answer,
        }
