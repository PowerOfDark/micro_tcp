class Event:
    def __init__(self):
        self._handlers = []

    def __iadd__(self, handler):
        self.subscribe(handler)
        return self

    def __isub__(self, handler):
        self.unsubscribe(handler)
        return self

    def invoke(self, *args, **kwargs):
        for handler in self._handlers:
            handler(*args, **kwargs)

    def subscribe(self, handler):
        self._handlers.append(handler)

    def unsubscribe(self, handler):
        self._handlers.remove(handler)

    def clear_obj(self, target: object):
        self._handlers = [h for h in self._handlers if getattr(h, 'im_self', False) != target]
