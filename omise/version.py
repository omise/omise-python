from importlib.metadata import version, PackageNotFoundError
try:
    __VERSION__ = version("omise")
except PackageNotFoundError:
    __VERSION__ = "unknown"