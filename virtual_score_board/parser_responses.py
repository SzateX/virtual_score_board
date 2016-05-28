from random import choice


class Response(object):
    def __init__(self, type_of_response, code_of_response, status, data=None):
        self.type_of_response = type_of_response
        self.code_of_response = code_of_response
        self.status = status
        self.data = data
        self.description = None

    def get_response(self):
        dictionary = {"type": self.type_of_response,
                      "code": self.code_of_response,
                      "status": self.status,
                      "data": self.data,
                      "description": self.description
                      }
        return dictionary


class EverythingGood(Response):
    def __init__(self, data=None):
        super(EverythingGood, self).__init__("Information", 1000, "EverythingGood", data)
        self.description = "The command has been executed correctly"


class CorrectCredentials(Response):
    def __init__(self, data=None):
        super(CorrectCredentials, self).__init__("Information", 1001, "CorrectCredentials", data)
        self.description = "The credentials have been given correct, you are logged"


class SignedOut(Response):
    def __init__(self, data=None):
        super(SignedOut, self).__init__("Information", 1002, "SignedOut", data)
        self.description = "I saw you want to log out. I fulfilled your request"


class Pong(Response):
    descriptions = ["Do you want to play table-tennis with me?", "Smash!", "You are very good!", "Pong",
                    "Are not you tired?", "Ha ha!", "1:0 for me!", "Girls will be throwing their bras for this!"]

    def __init__(self, data=None):
        super(Pong, self).__init__("Information", 1999, "Pong", data)
        self.description = choice(self.descriptions)


class NotLogged(Response):
    def __init__(self, data=None):
        super(NotLogged, self).__init__("Error", 3001, "NotLogged", data)
        self.description = "I can't do any actions. You need do sign in."


class WrongCredentials(Response):
    def __init__(self, data=None):
        super(WrongCredentials, self).__init__("Error", 3002, "WrongCredentials", data)
        self.description = "You have given me wrong login data. Please correct it."


class CurrentlyLogged(Response):
    def __init__(self, data=None):
        super(CurrentlyLogged, self).__init__("Error", 3003, "CurrentlyLogged", data)
        self.description = "You are currently logged. Why are you try to sign in twice?"


class NotJson(Response):
    def __init__(self, data=None):
        super(NotJson, self).__init__("Error", 3004, "NotJson", data)
        self.description = "You send data, which are not json. Please repair it!"


class CannotParse(Response):
    def __init__(self, description, data=None):
        super(CannotParse, self).__init__("Error", 3005, "CannotParse", data)
        self.description = description


class WrongDataType(Response):
    def __init__(self, description, data=None):
        super(WrongDataType, self).__init__("Error", 3006, "WrongDataType", data)
        self.description = description


class UnknownError(Response):
    def __init__(self, data=None):
        super(UnknownError, self).__init__("Error", 3999, "UnknownError", data)
        self.description = "Unknown Error"
