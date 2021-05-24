from marshmallow import EXCLUDE, Schema
from marshmallow.fields import DateTime, Int, Str


class NoteSerializer(Schema):
    id = Int(dump_only=True)
    name = Str(required=True)
    text = Str(required=True)
    creation_date = DateTime(dump_only=True)

    class Meta:
        unknown = EXCLUDE


class UserSerializer(Schema):
    username = Str(required=True)
    password = Str(required=True)

    class Meta:
        unknown = EXCLUDE
