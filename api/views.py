from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from .models import *
from django.contrib.auth.hashers import make_password
from . import json
from django.utils.crypto import get_random_string
from . import helpers
import socket
from django.core.exceptions import ObjectDoesNotExist
import smtplib
from email.mime.text import MIMEText
from rest_framework.response import Response
from rest_framework import generics
from django.core import serializers
from django.db import transaction
from django.db.models import Q

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
# Create your views here.


@csrf_exempt
@transaction.atomic
def login(request):
	import json as j
	requestData =  j.loads(request.body.decode('utf-8'))
	user = helpers.auth_user(requestData['username'], requestData['password'])
	# if user is None:
		# return json.Response('User name or Password Wrong', False)
	if user['status']:
		return json.Response(user['error_msg'], False)
	if user['user']:
		# generate token for authenticated user
		auth_token = helpers.auth_token(user['user'], request)
		if auth_token:
			auth_token['expiry'] = int(time.time())+36000			
			user_id=User.objects.get(username=requestData['username'])
			auth_token['username'] = requestData['username']
			StoreAuthtokenTbl = AuthTokenMstr(
				user_id=user_id,
				jwt_token=auth_token['token'],
				expire_ts=int(time.time())+36000,
				created_on=int(time.time())
			)
			StoreAuthtokenTbl.save()

			user_login_history = UserLoginHistory(
			user_id=user_id,
			jwt_token=auth_token['token'],
			login_time=int(time.time()),
			expire_ts=int(time.time())+36000,
			# ip=socket.gethostbyname(socket.gethostname()),
			created_on=int(time.time())
			)
			user_login_history.save()
			return json.Response(auth_token)
		else:
			transaction.set_rollback(True)
			return json.Response('Check Headers', False)
	else:
		return json.Response('User name or Password Wrong', False)
	return json.Response('')

class logout(generics.ListCreateAPIView):
	
	def get(self,request):			
		headers= request.META['HTTP_AUTHORIZATION']
		split_token = headers.split('Bearer ')		
		jwt_token = split_token[1]
		get_user = AuthTokenMstr.objects.get(jwt_token=jwt_token)
		if(get_user):
			user_data = AuthSeralizer(get_user)
			user_id = user_data.data['user_id']
			user_login_history = UserLoginHistory.objects.filter(user_id=user_id,jwt_token=jwt_token).update(logout_time=int(time.time()),modified_on=int(time.time()))
			return json.Response("Logout Successfully",True)
		else:
			return json.Response("Unable to get user",False)