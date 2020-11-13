from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from api.models import Customer
from django.http import Http404
import jwt
import json

def jwt_token(request):
	try:
		token = jwt.decode(request.headers['x-auth-token'], 'secret', algorithms=['HS256'])
	except Exception as e:
		return Response(str(e))

	customer = Customer.objects.filter(phone=token['phone']).first()

	if customer:
		return True
	else:
		return False

def returnResponse(request, data, status, code):
	response = {
		'success': status,
		'data': data,
	}
	return Response( response , status = code )
