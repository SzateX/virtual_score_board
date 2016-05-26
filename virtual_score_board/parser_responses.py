class Response(object):
    def __init__(self):
        self.type_of_response = None
        self.code_of_response = None
        self.status = None

    def get_response(self):
        dictionary = {"type": self.type_of_response,
                      "code": self.code_of_response,
                      "status": self.status
                      }
        return dictionary


class Status(object):
    pass


class EverythingGood(Status):
    pass


class CorrectCredentials(Status):
    pass


class SignMeOut(Status):
    pass


class Pong(Status):
    pass


class CurrentlyLogged(Status):
    pass


class NotLogged(Status):
    pass


class WrongCredentials(Status):
    pass
