from .constants import Constant
from src.models.blacklist import BlackList
from src.commands.base_command import BaseCommannd
from src.errors.errors import MissingRequiredField, MissingRequiredToken,InvalidFormatField,WrongSecretToken
import uuid, re



class AddEmail(BaseCommannd):
    def __init__(self, session, json_request, headers, ip_address) -> None:
        
        self.session = session
        if 'Authorization' not in headers:
            raise MissingRequiredToken()
        else:
            authorization_header = headers["Authorization"]
            if "Bearer" not in authorization_header:
                raise MissingRequiredToken()
            headers = {'Authorization': authorization_header}
            print(headers)
            print(authorization_header)
            token = authorization_header[7:len(authorization_header)]
            if token==Constant.SECRET_TOKEN:
                print(token)
            else:
                raise WrongSecretToken
        if ("email" not in json_request.keys() or
                "app_uuid" not in json_request.keys()):
            raise MissingRequiredField()
        
        email = json_request["email"]
        app_uuid = json_request["app_uuid"]
        blocked_reason = json_request["blocked_reason"]

         
        if email == "" or app_uuid == "" :
            raise MissingRequiredField

        try:
            uuid.UUID(str(app_uuid))
        except ValueError:
            raise InvalidFormatField

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if(re.fullmatch(regex, email) ):
            print(email)
        else:
            raise InvalidFormatField
    
        self.blacklist = BlackList(email=email,app_uuid=app_uuid,blocked_reason=blocked_reason, ip_address=ip_address)

    def execute(self):
        self.session.add(self.blacklist)
        self.session.commit()
        return "Se  agregado el email a la lista"
         
