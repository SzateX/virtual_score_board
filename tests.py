from unittest.mock import patch, Mock, MagicMock
from datetime import datetime, timedelta
from twisted.internet import task
from virtual_score_board.models import Timer, Counter, Team, Game, ReverseTimer, \
    TeamKeyError, ClockKeyError, CounterKeyError, User
from virtual_score_board.command_parser import Parser, ParseError
from virtual_score_board.parser_types import is_team, is_counter, is_clock, integer, string, boolean, ParserTypeError
import pytest

a = datetime(2015, 1, 25, 21, 55, 10)
b = a + timedelta(seconds=20)


# Test Timer
def test_timer_twenty_second():
    timer = Timer()
    with patch('virtual_score_board.models.datetime') as mock:
        mock.now = Mock(return_value=a)
        timer.start()

    with patch('virtual_score_board.models.datetime') as mock:
        mock.now = Mock(return_value=b)
        timer.end()

    assert int(timer.get_seconds()) == 20


def test_timer_reset_timer():
    timer = Timer()
    with patch('virtual_score_board.models.datetime') as mock:
        mock.now = Mock(return_value=a)
        timer.start()

    with patch('virtual_score_board.models.datetime') as mock:
        mock.now = Mock(return_value=b)
        timer.end()
    timer.reset_timer()
    assert int(timer.get_seconds()) == 0


def test_timer_is_enabled_when_start():
    timer = Timer()
    timer.start()
    assert timer.is_enabled is True


def test_timer_is_disables_when_end():
    timer = Timer()
    timer.end()
    assert timer.is_enabled is False


# Test ReverseTimer
def test_reverse_timer_is_enabled_when_start():
    timer = ReverseTimer(20)
    with patch('virtual_score_board.models.reactor', new=task.Clock()) as clock:
        timer.start()
    assert timer.is_enabled is True


def test_reverse_timer_twenty_second_stop():
    timer = ReverseTimer(20)
    with patch('virtual_score_board.models.reactor', new=task.Clock()) as clock:
        timer.start()
        clock.advance(20)

    assert timer.is_enabled is False


def test_reverse_timer_set_max_seconds():
    timer = ReverseTimer(20)
    timer.set_max_seconds(40)
    assert timer.max_seconds == 40


# Test Counter
def test_counter_is_zero_when_init():
    counter = Counter()
    assert counter.points == 0


def test_counter_one_point():
    counter = Counter()
    counter.add_point()
    assert counter.points == 1


def test_counter_two_points():
    counter = Counter()
    counter.add_point(2)
    assert counter.points == 2


def test_counter_reset_points():
    counter = Counter()
    counter.points = 15
    counter.reset_points()
    assert counter.points == 0


def test_counter_subtract_one_point():
    counter = Counter()
    counter.points = 30
    counter.subtract_point()
    assert counter.points == 29


def test_counter_subtract_two_points():
    counter = Counter()
    counter.points = 10
    counter.subtract_point(2)
    assert counter.points == 8


def test_counter_zero_when_tried_subtract_more_then_i_have():
    counter = Counter()
    counter.points = 1
    counter.subtract_point(3)
    assert counter.points == 0


# Test Team
def test_team_name_on_init_is_foo():
    team = Team()
    assert team.name == "Foo"


def test_team_timeout_flag_on_init_is_disabled():
    team = Team()
    assert team.timeout_flag is False


def test_team_penalty_flag_on_init_is_disabled():
    team = Team()
    assert team.penalty_flag is False


def test_team_get_counter_in_case_regular():
    team = Team()
    assert team.get_counter("regular") is team.points


def test_team_get_counter_in_case_set():
    team = Team()
    assert team.get_counter("set") is team.set_points


def test_team_get_counter_what_in_fail():
    team = Team()
    with pytest.raises(CounterKeyError) as excinfo:
        team.get_counter("pig")
    assert "Only 'regular' or 'set' key is permitted" in str(excinfo.value)


# Test Game
def test_game_to_dict():
    game = Game()
    temp_dict = {
        'home_name': "Foo",
        'home_points': 0,
        'home_set_points': 0,
        'home_penalty': False,
        'home_timeout': False,
        'away_name': "Foo",
        'away_points': 0,
        'away_set_points': 0,
        'away_penalty': False,
        'away_timeout': False,
        'match_seconds': 0,
        'match_twenty_four_seconds': 0,
        'match_period': 1
    }
    assert game.to_dict() == temp_dict


def test_game_get_team_in_case_home():
    game = Game()
    assert game.get_team("home") is game.home_team


def test_game_get_team_in_case_away():
    game = Game()
    assert game.get_team("away") is game.away_team


def test_game_get_team_what_in_fail():
    game = Game()
    with pytest.raises(TeamKeyError) as excinfo:
        game.get_team("cow")
    assert "Only 'home' or 'away' key is permitted" in str(excinfo.value)


def test_game_get_clock_in_case_match():
    game = Game()
    assert game.get_clock("match") is game.match_clock


def test_game_get_clock_in_case_twenty_four():
    game = Game()
    assert game.get_clock("twenty_four") is game.twenty_four_clock


def test_game_get_clock_what_in_fail():
    game = Game()
    with pytest.raises(ClockKeyError) as excinfo:
        game.get_clock("duck")
    assert "Only 'match' or 'twenty_four' key is permitted" in str(excinfo.value)


# Test parser types
def test_is_team_in_case_home():
    what_returned = is_team("home")
    assert what_returned is None


def test_is_team_in_case_away():
    what_returned = is_team("away")
    assert what_returned is None


def test_is_team_in_case_fail():
    with pytest.raises(ParserTypeError) as excinfo:
        is_team("fail")
    assert "Only 'home' or 'away' permitted." in str(excinfo.value)


def test_is_clock_in_case_match():
    what_returned = is_clock("match")
    assert what_returned is None


def test_is_clock_in_case_twenty_four():
    what_returned = is_clock("twenty_four")
    assert what_returned is None


def test_is_clock_in_case_fail():
    with pytest.raises(ParserTypeError) as excinfo:
        is_clock("fail")
    assert "Only 'match' or 'twenty_four' permitted." in str(excinfo.value)


def test_is_counter_in_case_regular():
    what_returned = is_counter("regular")
    assert what_returned is None


def test_is_counter_in_case_set():
    what_returned = is_counter("set")
    assert what_returned is None


def test_is_counter_in_case_fail():
    with pytest.raises(ParserTypeError) as excinfo:
        is_counter("fail")
    assert "Only 'regular' or 'set' permitted." in str(excinfo.value)


def test_integer():
    what_returned = integer(3)
    assert what_returned is None


def test_integer_in_fail_case():
    with pytest.raises(ParserTypeError) as excinfo:
        integer("fail")
    assert "Value is not integer:" in str(excinfo.value)


def test_string():
    what_returned = string("Foo")
    assert what_returned is None


def test_string_in_fail_case():
    with pytest.raises(ParserTypeError) as excinfo:
        string({'fail': 'fail'})
    assert "Value is not string:" in str(excinfo.value)


def test_boolean():
    what_returned = boolean(False)
    assert what_returned is None


def test_boolean_in_fail_case():
    with pytest.raises(ParserTypeError) as excinfo:
        boolean("Fail")
    assert "Value is not boolean:" in str(excinfo.value)


# Test Parser
def create_game():
    game = Game()
    game.home_team.points = MagicMock()
    game.home_team.set_points = MagicMock()
    game.away_team.points = MagicMock()
    game.away_team.set_points = MagicMock()
    game.match_clock = MagicMock()
    game.twenty_four_clock = MagicMock()
    game.period = MagicMock()
    return game


def test_parser_in_wrong_command_case():
    data = {"cmd": "wrong_command"}
    parser = Parser(MagicMock)
    with pytest.raises(ParseError) as excinfo:
        parser.parse_and_execute(data, MagicMock)
    assert "No command found:" in str(excinfo.value)


def test_parser_with_less_args_case():
    data = {"cmd": "clock_stop"}
    parser = Parser(MagicMock)
    with pytest.raises(ParseError) as excinfo:
        parser.parse_and_execute(data, MagicMock)
    assert "I need" in str(excinfo.value)


def test_parser_with_too_much_args_case():
    data = {"cmd": "clock_stop",
            "clock": "regular",
            "arg": "soap"}
    parser = Parser(MagicMock)
    with pytest.raises(ParseError) as excinfo:
        parser.parse_and_execute(data, MagicMock)
    assert "Too many arguments:" in str(excinfo.value)


def test_parser_clock_stop():
    data = {"cmd": "clock_stop",
            "clock": "match"}
    parser = Parser(create_game())
    parser.parse_and_execute(data, MagicMock)
    parser.game.match_clock.end.assert_called_with()


def test_parser_clock_start():
    data = {"cmd": "clock_start",
            "clock": "twenty_four"}
    parser = Parser(create_game())
    parser.parse_and_execute(data, MagicMock)
    parser.game.twenty_four_clock.start.assert_called_with()


def test_parser_clock_reset():
    data = {"cmd": "clock_reset",
            "clock": "twenty_four"}
    parser = Parser(create_game())
    parser.parse_and_execute(data, MagicMock)
    parser.game.twenty_four_clock.reset_clock.assert_called_with()


def test_parser_clock_set_max_seconds():
    data = {"cmd": "clock_set_seconds",
            "clock": "match",
            "arg": 30}
    parser = Parser(create_game())
    parser.parse_and_execute(data, MagicMock)
    parser.game.match_clock.set_max_seconds.assert_called_with(30)


def test_parser_set_name():
    data = {"cmd": "set_name",
            "team": "home",
            "arg": "Foo"}
    parser = Parser(create_game())
    parser.parse_and_execute(data, MagicMock)
    assert parser.game.home_team.name == "Foo"


def test_parser_set_timeout_flag():
    data = {"cmd": "set_timeout_flag",
            "team": "away",
            "arg": True}
    parser = Parser(create_game())
    parser.parse_and_execute(data, MagicMock)
    assert parser.game.away_team.timeout_flag is True


def test_parser_set_penalty_flag():
    data = {"cmd": "set_penalty_flag",
            "team": "home",
            "arg": False}
    parser = Parser(create_game())
    parser.parse_and_execute(data, MagicMock)
    assert parser.game.home_team.penalty_flag is False


def test_points_add():
    data = {"cmd": "points_add",
            "counter": "regular",
            "team": "away",
            "arg": 3}
    parser = Parser(create_game())
    parser.parse_and_execute(data, MagicMock)
    parser.game.away_team.points.add_point.assert_called_with(3)


def test_points_subtract():
    data = {"cmd": "points_subtract",
            "counter": "set",
            "team": "home",
            "arg": 2}
    parser = Parser(create_game())
    parser.parse_and_execute(data, MagicMock)
    parser.game.home_team.set_points.subtract_point.assert_called_with(2)


def test_points_set():
    data = {"cmd": "points_set",
            "counter": "regular",
            "team": "away",
            "arg": 69}
    parser = Parser(create_game())
    parser.parse_and_execute(data, MagicMock)
    parser.game.away_team.points.set_points.assert_called_with(69)


def test_points_reset():
    data = {"cmd": "points_reset",
            "counter": "set",
            "team": "home"}
    parser = Parser(create_game())
    parser.parse_and_execute(data, MagicMock)
    parser.game.home_team.set_points.reset_points.assert_called_with()


def test_period_set():
    data = {"cmd": "period_set",
            "arg": 2}
    parser = Parser(create_game())
    parser.parse_and_execute(data, MagicMock)
    parser.game.period.set_points.assert_called_with(2)
