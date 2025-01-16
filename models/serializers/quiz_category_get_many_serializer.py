from marshmallow import Schema, fields, post_load
from models.quiz_category import QuizCategory


class QuizCategoryGetManySerializer(Schema):
    id = fields.UUID(required=False, allow_none=True)  # UUID will be auto-generated if not provided
    name = fields.Str(required=True)  # Category name is required

    @post_load
    def make_quiz_category(self, data, **kwargs):
        """Convert the deserialized data into a QuizCategory model instance."""
        return QuizCategory(**data)
