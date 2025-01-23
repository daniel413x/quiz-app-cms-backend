from marshmallow import Schema, fields, post_load
from models.quiz_category import QuizCategory


class QuizCategoryGetManySerializer(Schema):
    id = fields.UUID(required=False, allow_none=True)
    name = fields.Str(required=True)
    slug = fields.Str(required=True)

    @post_load
    def make_quiz_category(self, data, **kwargs):
        return QuizCategory(**data)
