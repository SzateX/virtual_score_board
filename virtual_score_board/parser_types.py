from virtual_score_board.models import User

class ParserTypeError(Exception):
    pass


def is_team(value):
    if value not in ("home", "away"):
        raise ParserTypeError("Only 'home' or 'away' permitted. Recived: %s" % value)


def is_clock(value):
    if value not in ("match", "twenty_four"):
        raise ParserTypeError("Only 'match' or 'twenty_four' permitted. Recived: %s" % value)


def is_counter(value):
    if value not in ("regular", "set"):
        raise ParserTypeError("Only 'regular' or 'set' permitted. Recived: %s" % value)


def integer(value):
    if not isinstance(value, int):
        raise ParserTypeError("Value is not integer: %s" % value)


def string(value):
    if not isinstance(value, str):
        raise ParserTypeError("Value is not string: %s" % value)


def boolean(value):
    if not isinstance(value, bool):
        raise ParserTypeError("Value is not boolean: %s" % value)


def is_user(value):
    if not isinstance(value, User) or value is None:
        raise ParserTypeError("Only User instance or None value permitted!")


def integer_range(a, b):
    def inner(value):
        integer(value)
        if value not in range(a, b):
            raise ParserTypeError("Integer is not in range %d-%d" % (a, b))

    return inner
