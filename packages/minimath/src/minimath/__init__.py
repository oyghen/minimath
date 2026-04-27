__all__ = ("__version__", "core", "fn", "seq")

from importlib import metadata

from minimath import core, fn, seq

__version__ = metadata.version(__name__)
