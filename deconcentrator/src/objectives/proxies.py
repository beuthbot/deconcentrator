import base64


class ObjectiveProxy(object):
    """ proxy class to allow easier access to virtual properties.
    """

    _objective = None

    def __init__(self, objective):
        self._objective = objective

    def __getattr__(self, attr):
        if attr in ("type", "data"):
            payload_type = self._objective.payload.get(attr)

            if attr == "type":
                return payload_type

            return base64.standard_b64decode(self._objective.payload["data"])

        return getattr(self._objective, attr)
