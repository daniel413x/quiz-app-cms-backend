import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID


class QuizCategory(db.Model):
    __tablename__ = "quiz_category"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # Relationship: A category has many quizzes
    quizzes = db.relationship('Quiz', back_populates='category', cascade="all, delete", lazy=True)

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
        }
