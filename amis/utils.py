from functools import partial

try:
    import ujson  # type: ignore

    json_loads = ujson.loads
    json_dumps = partial(
        ujson.dumps,
        ensure_ascii=False,
        indent=4,
        escape_forward_slashes=False,
    )
except ImportError:
    import json

    json_loads = json.loads
    json_dumps = partial(
        json.dumps,
        ensure_ascii=False,
        indent=4,
    )
