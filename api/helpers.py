import json
from django.http import request
from .models import *
from .serializers import *
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
import time

def expect_urls():
    urls = [
    '/api/login/',    
    ]
    return urls

def relative_urls():
    urls = [
        
       "(\/api\/reset_pwd\/)(?P<string>.+)$",
       "(\/media\/)",
    ]
    return urls

def header(request):
    auth = request.META.get('HTTP_AUTHORIZATION')
    if auth:
        auth = auth.split()
    if auth and auth[1]:
        return auth[1]

    return False;

def auth_token(user,request):
   refresh = RefreshToken.for_user(user)
   user = User.objects.get(username=user)
   return {"token": str(refresh.access_token)}

def auth_user(username,pwd):
    try:
        user = User.objects.get(username = username)
    except:
        user = None
        return {"status":True,"error_msg" : "Invalid User Credentials"}
    if user:
        try:
            user = User.objects.get(username = username,is_active=True)
            is_match = user.check_password(pwd)
            if is_match:
                return {"user":user,"status":False}
            else:
                return {"status":True,"error_msg" : "Invalid User Credentials"}
        except:
            return {"status":True,"error_msg" : "Account Activation Failed,Please contact Admin to activate"}
           
    return None;


#convert unix timestamp to readable format
def convert_epoch_to_dt(date):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date))