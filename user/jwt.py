from rest_framework.authentication import get_authorization_header,BaseAuthentication
from rest_framework import exceptions
import jwt
from .models import User
from django.conf import settings
class JWTAuthentication(BaseAuthentication):
    def authenticate(self,request):
        auth_header = get_authorization_header(request)

        auth_data = auth_header.decode('utf-8')

        auth_token = auth_data.split(" ")
        if auth_token[0] == "":
            pass
        else:
            if len(auth_token) != 2 and len(auth_token) != 0:
                print(auth_token)
                raise exceptions.AuthenticationFailed("Wrong Token")
            token = auth_token[1]

            try:
                payload = jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
                username = payload['username']

                user = User.objects.get(username = username)
                return (user, token)
                
            except jwt.ExpiredSignatureError as ex:
                raise exceptions.AuthenticationFailed("Token has expired Login again")
            
            except jwt.DecodeError as ex:
                raise exceptions.AuthenticationFailed("Token is invalid")
            
            except User.DoesNotExist as no_user:
                raise exceptions.AuthenticationFailed("User does not exist")