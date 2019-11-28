class Serializer:
    """
    Abstract base class for wire serializers
    """
    def __init__(self):
        pass

    def serialize(self, payload):
        pass

    def deserialize(self, payload):
        pass
