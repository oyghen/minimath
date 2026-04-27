__all__ = ("__version__", "core", "seq")

from importlib import metadata

from minimath import core, seq

__version__ = metadata.version(__name__)
