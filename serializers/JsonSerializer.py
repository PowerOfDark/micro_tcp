import json

from serializers.Serializer import Serializer


class JsonSerializer(Serializer):
    def __init__(self):
        super().__init__()

    def serialize(self, payload):
        return json.dumps(payload)

    def deserialize(self, payload):
        return json.loads(payload)

