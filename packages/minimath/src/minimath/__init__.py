__all__ = ("__version__", "core", "fn", "seq", "sets")

from importlib import metadata

from minimath import core, fn, seq, sets

__version__ = metadata.version(__name__)
