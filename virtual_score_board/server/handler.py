from autobahn.twisted.websocket import WebSocketServerProtocol
from twisted.internet.defer import Deferred
from twisted.internet import task, reactor
from virtual_score_board.models import Game, User
from virtual_score_board.command_parser import Parser, ParseError
from virtual_score_board.parser_types import ParserTypeError
from virtual_score_board.parser_responses import CorrectCredentials, SignedOut, CannotParse,\
    WrongDataType, UnknownError, NotJson
import json

game = Game()

template_dict = {
    'home_name': 'Foo',
    'home_score': 0,
    'home_penalty': False,
    'home_timeout': False,
    'away_name': 'Bar',
    'away_score': 0,
    'away_penalty': False,
    'away_timeout': False,
    'match_seconds': 350,
    'match_period': 1
}


class ServerHandler(WebSocketServerProtocol):
    second_deffer = None
    parser = Parser(game)

    def __init__(self):
        super(ServerHandler, self).__init__()
        self.user = None

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        self.send_data_for_second()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
            message = payload.decode('utf8')
            try:
                data = json.loads(message)
            except ValueError:
                self.send_response(NotJson())
                return
            try:
                response = self.parser.parse_and_execute(data, self.user)
                if isinstance(response, CorrectCredentials):
                    self.user = User()
                elif isinstance(response, SignedOut):
                    self.user = None
                self.send_response(response)
            except ParseError as e:
                self.send_response(CannotParse(str(e)))
            except ParserTypeError as e:
                self.send_response(WrongDataType(str(e)))
            except:
                self.send_response(UnknownError())

    def onClose(self, wasClean, code, reason):
        if self.second_deffer is not None:
            self.second_deffer.cancel()
        print("WebSocket connection closed: {0}".format(reason))

    def send_data(self):
        dictionary = game.to_dict()
        dictionary["logged"] = True if self.user else False
        data = {"data": dictionary}
        state = json.dumps(data)
        self.sendMessage(state.encode('utf-8'), isBinary=False)

    def send_data_for_second(self):
        self.send_data()
        self.second_deffer = task.deferLater(reactor, 1.0, self.send_data_for_second)

    def send_response(self, response_object):
        data = {"response": response_object.get_response()
                }
        state = json.dumps(data)
        self.sendMessage(state.encode('utf-8'), isBinary=False)
