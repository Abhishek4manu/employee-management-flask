from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=4, max=50))
    password = fields.String(required=True, validate=validate.Length(min=6))
