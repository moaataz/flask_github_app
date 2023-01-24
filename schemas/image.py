from werkzeug.datastructures import FileStorage
from marshmallow import Schema,fields

class ImageField(fields.Field):
    default_error_messages = {'error':'image error'}
    def _deserialize(self, value, attr, data):
        if value is None:
            return None
        if not isinstance(value,FileStorage):
            self.fail('error')
        return value
class ImageSchema(Schema):
    image = ImageField(required=True)