import enum


class ViewType(enum.Enum):
    LOGIN = 1,
    REGISTER = 2,
    MENU = 3,
    UPLOAD = 4,
    FILE_LIST = 5,
    SHARED_FILES = 6,
    TRASHED_FILES = 7
