"""FANTASIA — A terminal-native AI operator modeled after The NeverEnding Story.

DO WHAT THOU WILT. Keep the memory before The Nothing claims the rest.
"""

__version__ = "0.1.0"
__author__ = "jer <jeremedotxyz@gmail.com>"

from fantasia.auryn import Auryn, Wish
from fantasia.nothing import NothingGauge
from fantasia.oracle import SouthernOracle
from fantasia.ui import TerminalRenderer

__all__ = [
    "Auryn",
    "Wish",
    "NothingGauge",
    "SouthernOracle",
    "TerminalRenderer",
    "__version__",
]
