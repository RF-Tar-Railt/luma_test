import sys

if sys.version_info >= (3, 11):
    import tomllib  # noqa
else:
    import tomli as tomllib  # noqa


if sys.version_info >= (3, 10):
    import importlib.metadata as importlib_metadata  # noqa
else:
    import importlib_metadata  # noqa


Distribution = importlib_metadata.Distribution


__all__ = [
    "tomllib",
    "importlib_metadata",
    "Distribution",
]