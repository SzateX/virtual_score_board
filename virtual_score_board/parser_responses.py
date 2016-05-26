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
