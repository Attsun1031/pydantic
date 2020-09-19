from schematics import __version__, Model
from schematics.exceptions import DataError, ValidationError
from schematics.types import FloatType, StringType, IntType, DateTimeType, ModelType, ListType


class TestSchematics:
    package = 'schematics'
    version = __version__

    def __init__(self, allow_extra):
        class LocationSchema(Model):
            latitude = FloatType(required=False)
            longitude = FloatType(required=False)

        class SkillSchema(Model):
            subject = StringType(required=True)
            subject_id = IntType(required=True)
            category = StringType(required=True)
            qual_level = StringType(required=True)
            qual_level_id = IntType(required=True)
            qual_level_ranking = FloatType(default=0)

        class ExampleModel(Model):
            id = IntType(required=True)
            client_name = StringType(max_length=255, required=True)
            sort_index = FloatType(required=True)
            # client_email = fields.Email()
            client_phone = StringType(max_length=255, required=False)

            location = ModelType(LocationSchema)

            contractor = IntType(min_value=0, required=False)
            upstream_http_referrer = StringType(max_length=1023, required=False)
            grecaptcha_response = StringType(max_length=1000, min_length=20, required=True)
            last_updated = DateTimeType(required=False, formats="%Y-%m-%dT%H:%M:%S")
            skills = ListType(ModelType(SkillSchema))

        self.allow_extra = allow_extra  # unused
        self.schema = ExampleModel

    def validate(self, data):
        try:
            result = self.schema(data).validate()
        except DataError as e:
            return False, e.errors
        except ValidationError as e:
            return False, e.errors
        else:
            return True, result
