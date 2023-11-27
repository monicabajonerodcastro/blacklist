
from .constants import Constant
from src.models.blacklist import BlackList
from src.commands.base_command import BaseCommannd
from src.errors.errors import MissingRequiredToken,WrongSecretToken


class ValidateEmail(BaseCommannd):

    def __init__(self, session, headers, email):

        self.session = session

        if 'Authorization' not in headers:
            raise MissingRequiredToken()
        else:
            authorization_header = headers["Authorization"]
            if "Bearer" not in authorization_header:
                raise MissingRequiredToken()
            token = authorization_header[7:len(authorization_header)]
            if token!=Constant.SECRET_TOKEN:
                raise WrongSecretToken

        result_email = self.session.query(BlackList).filter(BlackList.email == email).first()
        self.result_email = result_email
        
                
    def execute(self):
        return self.result_email is not None
