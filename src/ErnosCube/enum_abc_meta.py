from enum import Enum
from abc import ABC


class EnumABCMeta(type(Enum), type(ABC)):
    """Meta-class for Enum's that also inherit from classes derived from ABC"""

    pass
