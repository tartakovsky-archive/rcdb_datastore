import orjson


class CustomJSONEncoderMixin:
    json_loads = orjson.loads
    json_dumps = lambda v, *, default: orjson.dumps(v, default=default).decode()
