from datetime import datetime
from twisted.internet.defer import Deferred
from twisted.internet import task, reactor


class TeamKeyError(Exception):
    pass


class ClockKeyError(Exception):
    pass


class CounterKeyError(Exception):
    pass


class Counter(object):
    def __init__(self, initial_points=0):
        self.points = initial_points

    def add_point(self, how_many=1):
        self.points += how_many

    def subtract_point(self, how_many=1):
        if (self.points - how_many) <= 0:
            self.points = 0
        else:
            self.points -= how_many

    def set_points(self, how_many):
        self.points = how_many

    def reset_points(self):
        self.points = 0

    def get_points(self):
        return self.points


class Timer(object):
    seconds_from_last_action = 0
    is_enabled = False
    timestamp = None

    def __init__(self):
        self.timestamp = datetime.now()

    def start(self):
        if not self.is_enabled:
            self.is_enabled = True
            self.timestamp = datetime.now()

    def end(self):
        if self.is_enabled:
            self.is_enabled = False
            delta = datetime.now() - self.timestamp
            self.seconds_from_last_action += delta.total_seconds()

    def reset_timer(self):
        self.seconds_from_last_action = 0
        self.timestamp = datetime.now()

    def get_seconds(self):
        if self.is_enabled:
            delta = datetime.now() - self.timestamp
            return self.seconds_from_last_action + delta.total_seconds()
        return self.seconds_from_last_action


class ReverseTimer(Timer):
    def __init__(self, seconds):
        super(ReverseTimer, self).__init__()
        self.deffer = None
        self.max_seconds = seconds

    def start(self):
        delta = self.max_seconds - self.get_seconds()
        self.deffer = task.deferLater(reactor, delta, self.end)
        super(ReverseTimer, self).start()

    def end(self):
        super(ReverseTimer, self).end()
        if self.deffer is not None:
            self.deffer.cancel()

    def reset_state(self):
        self.end()
        self.reset_timer()

    def reset_clock(self):
        self.reset_state()
        self.start()

    def get_remaining_seconds(self):
        return self.max_seconds - self.get_seconds()

    def set_max_seconds(self, seconds):
        self.reset_state()
        self.max_seconds = seconds


class Team(object):
    def __init__(self):
        self.name = "Foo"
        self.points = Counter()
        self.set_points = Counter()
        self.timeout_flag = False
        self.penalty_flag = False

    def get_counter(self, key):
        if key == "regular":
            return self.points
        elif key == "set":
            return self.set_points
        else:
            raise CounterKeyError("Only 'regular' or 'set' key is permitted")


class Game(object):
    def __init__(self):
        self.home_team = Team()
        self.away_team = Team()
        self.match_clock = ReverseTimer(0)
        self.twenty_four_clock = ReverseTimer(0)
        self.period = Counter(1)

    def to_dict(self):
        temp_dict = {
            'home_name': self.home_team.name,
            'home_points': self.home_team.points.get_points(),
            'home_set_points': self.home_team.set_points.get_points(),
            'home_penalty': self.home_team.penalty_flag,
            'home_timeout': self.home_team.timeout_flag,
            'away_name': self.away_team.name,
            'away_points': self.away_team.points.get_points(),
            'away_set_points': self.away_team.set_points.get_points(),
            'away_penalty': self.away_team.penalty_flag,
            'away_timeout': self.away_team.timeout_flag,
            'match_seconds': self.match_clock.get_remaining_seconds(),
            'match_twenty_four_seconds': self.twenty_four_clock.get_remaining_seconds(),
            'match_period': self.period.get_points()
        }
        return temp_dict

    def get_team(self, key):
        if key == 'home':
            return self.home_team
        elif key == 'away':
            return self.away_team
        else:
            raise TeamKeyError("Only 'home' or 'away' key is permitted")

    def get_clock(self, key):
        if key == 'match':
            return self.match_clock
        elif key == 'twenty_four':
            return self.twenty_four_clock
        else:
            raise ClockKeyError("Only 'match' or 'twenty_four' key is permitted")


class User(object):
    def __init__(self):
        pass