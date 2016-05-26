class Response(object):
    def __init__(self, type_of_response, code_of_response, status, data=None):
        self.type_of_response = type_of_response
        self.code_of_response = code_of_response
        self.status = status
        self.data = data

    def get_response(self):
        dictionary = {"type": self.type_of_response,
                      "code": self.code_of_response,
                      "status": self.status,
                      "data": self.data
                      }
        return dictionary


class EverythingGood(Response):
    def __init__(self, data=None):
        super(EverythingGood, self).__init__("Information", 1000, "EverythingGood", data)


class CorrectCredentials(Response):
    def __init__(self, data=None):
        super(CorrectCredentials, self).__init__("Information", 1001, "CorrectCredentials", data)


class SignedOut(Response):
    def __init__(self, data=None):
        super(SignedOut, self).__init__("Information", 1002, "SignedOut", data)


class Pong(Response):
    def __init__(self, data=None):
        super(Pong, self).__init__("Information", 1999, "Pong", data)


class NotLogged(Response):
    def __init__(self, data=None):
        super(NotLogged, self).__init__("Error", 3001, "NotLogged", data)


class WrongCredentials(Response):
    def __init__(self, data=None):
        super(WrongCredentials, self).__init__("Error", 3002, "WrongCredentials", data)


class CurrentlyLogged(Response):
    def __init__(self, data=None):
        super(CurrentlyLogged, self).__init__("Error", 3003, "CurrentlyLogged", data)