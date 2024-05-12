import enum

from view.login import *


class ViewType(enum.Enum):
    LOGIN = 1,
    MENU = None,
    UPLOAD = None,
    FILE_LIST = None,
