import re


class Validate:
    def __init__(self):
        self.regex_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    def validate_exist(self, inp):

        if not inp:
            return False
        return True

    def validate_length(self, inp, length):
        if not self.validate_exist(inp) or len(inp) < length:
            return False
        return True

    def validate_email(self, inp):
        if not self.validate_exist(inp) or not (re.search(self.regex_email, inp)):
            return False
        return True
