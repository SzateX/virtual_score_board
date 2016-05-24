from virtual_score_board.parser_types import integer, is_team, is_clock, is_counter, string, boolean, is_user
from passlib.hash import pbkdf2_sha256


class ParseError(Exception):
    pass


class NotLogged(Exception):
    pass


class WrongCredentials(Exception):
    pass


class HoorayCorrectCredentials(Exception):
    pass


class SignMeOut(Exception):
    pass


class Parser(object):
    def __init__(self, game_object):
        self.game = game_object

    def validate(self, command, args):
        extra_args = set(args) - set(command.__annotations__)
        if extra_args:
            raise ParseError("Too many arguments: %s" % extra_args)
        for key, type_func in command.__annotations__.items():
            try:
                type_func(args[key])
            except KeyError:
                raise ParseError("I need '%s' motherfucker" % key)

    def parse_and_execute(self, message_dict, user):
        try:
            command = getattr(self, 'command_%s' % message_dict['cmd'].strip().lower(), None)
        except KeyError:
            raise ParseError("I don't see 'cmd' key!")
        if command is None:
            raise ParseError('No command found: %s' % message_dict['cmd'])
        message_dict.pop('cmd')
        self.validate(command, message_dict)
        return command(user=user, **message_dict)

    def command_clock_stop(self, clock: is_clock, user):
        if not user:
            raise NotLogged("Not Logged!")
        clock = self.game.get_clock(clock)
        clock.end()
        return "OK"

    def command_clock_start(self, clock: is_clock, user):
        if not user:
            raise NotLogged("Not Logged!")
        clock = self.game.get_clock(clock)
        clock.start()
        return "OK"

    def command_clock_reset(self, clock: is_clock, user):
        if not user:
            raise NotLogged("Not Logged!")
        clock = self.game.get_clock(clock)
        clock.reset_clock()
        return "OK"

    def command_clock_set_seconds(self, clock: is_clock, arg: integer, user):
        if not user:
            raise NotLogged("Not Logged!")
        clock = self.game.get_clock(clock)
        clock.set_max_seconds(arg)
        return "OK"

    def command_set_name(self, team: is_team, arg: string, user):
        if not user:
            raise NotLogged("Not Logged!")
        team = self.game.get_team(team)
        team.name = arg
        return "OK"

    def command_set_timeout_flag(self, team: is_team, arg: boolean, user):
        if not user:
            raise NotLogged("Not Logged!")
        team = self.game.get_team(team)
        team.timeout_flag = not team.timeout_flag
        return "OK"

    def command_set_penalty_flag(self, team: is_team, arg: boolean, user):
        if not user:
            raise NotLogged("Not Logged!")
        team = self.game.get_team(team)
        team.penalty_flag = not team.timeout_flag
        return "OK"

    def command_points_add(self, counter: is_counter, team: is_team, arg: integer, user):
        if not user:
            raise NotLogged("Not Logged!")
        team = self.game.get_team(team)
        points = team.get_counter(counter)
        points.add_point(arg)
        return "OK"

    def command_points_subtract(self, counter: is_counter, team: is_team, arg: integer, user):
        if not user:
            raise NotLogged("Not Logged!")
        team = self.game.get_team(team)
        points = team.get_counter(counter)
        points.subtract_point(arg)
        return "OK"

    def command_points_set(self, counter: is_counter, team: is_team, arg: integer, user):
        if not user:
            raise NotLogged("Not Logged!")
        team = self.game.get_team(team)
        points = team.get_counter(counter)
        points.set_points(arg)
        return "OK"

    def command_points_reset(self, counter: is_counter, team: is_team, user):
        if not user:
            raise NotLogged("Not Logged!")
        team = self.game.get_team(team)
        points = team.get_counter(counter)
        points.reset_points()
        return "OK"

    def command_period_set(self, arg: integer, user):
        if not user:
            raise NotLogged("Not Logged!")
        self.game.period.set_points(arg)
        return "OK"

    def command_sign_in(self, login: string, password: string, user):
        with open("/var/passwords/pass.txt") as password_file:
            hashes = password_file.readlines()
            for line in hashes:
                username, hashed = line.split()
                if username == login:
                    if pbkdf2_sha256.verify(password, hashed):
                        return "CorrectCredentials"
            raise WrongCredentials("The credentials are wrong! Not logged!")

    def command_sign_out(self, user):
        return "SignMeOut"
