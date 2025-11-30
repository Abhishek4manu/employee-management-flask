from marshmallow import Schema, fields, validate

class EmployeeCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    age = fields.Integer(required=True, validate=validate.Range(min=18, max=70))
    email = fields.Email(required=True)
    department = fields.String(required=True, validate=validate.Length(min=2))
    salary = fields.Float(required=True, validate=validate.Range(min=1000, max=10000000))


class EmployeeUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(min=2, max=100))
    age = fields.Integer(validate=validate.Range(min=18, max=70))
    email = fields.Email()
    department = fields.String(validate=validate.Length(min=2))
    salary = fields.Float(validate=validate.Range(min=1000, max=10000000))
