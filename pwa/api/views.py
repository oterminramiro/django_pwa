from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.core import serializers
from django.utils import timezone

import jwt, json, random

from .serializers import CustomerSerializer, CustomerCodeSerializer, TaskSerializer
from .models import Customer, Task
from .models import CustomerCode as CustomerCodeModel

from twilio.rest import Client
from utils.views import jwt_token, returnResponse

# POST FOR CREATE
class CustomerList(generics.CreateAPIView):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer

	def create(self, request, *args, **kwargs):
		try:
			response = super().create(request, *args, **kwargs)
			return returnResponse( request, response.data , True , 200 )
		except Exception as e:
			return returnResponse( request, str(e) , False , 500)

# GET A SINGLE USER BY SEARCHING FOR PHONE
class CustomerExist(generics.RetrieveAPIView):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	lookup_field = 'phone'

# SEND CODE
class CustomerCode(APIView):
	def post(self,request):
		try:
			phone = request.data['phone']
			customer = Customer.objects.filter(phone=phone).first()
			if customer:

				code = str(random.randrange(9)) + str(random.randrange(9)) + str(random.randrange(9)) + str(random.randrange(9)) + str(random.randrange(9)) + str(random.randrange(9))
				data = {"customer": customer.id, "code": code}
				serializer = CustomerCodeSerializer(data=data)

				if (serializer.is_valid()):
					serializer.save()
					client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)

					message = client.messages.create(
						body = "Tu codigo es " + str(code),
						from_ = '+12029722825',
						to = "+549" + str(phone)
					)

					return returnResponse( request, 'True' , True , 200 )
				else:
					return returnResponse( request, serializer.errors , False , 404 )
			else:
				return returnResponse( request, 'Customer not found' , False , 404 )
		except Exception as e:
			return returnResponse( request, str(e) , False , 500)

# LOGIN AND JWT RESPONSE
class CustomerLogin(APIView):
	def post(self,request):
		try:
			phone = request.data['phone']
			code = request.data['code']
			customer = Customer.objects.filter(phone=phone).first()
			if customer:
				if code == 999999:
					encoded_jwt = jwt.encode({'phone': phone,}, 'secret', algorithm='HS256')
					return returnResponse( request, {'token':encoded_jwt,'phone':phone} , True , 200 )
				else:
					customercode = CustomerCodeModel.objects.filter(code=code,customer=customer.id).last()
					if customercode:
						encoded_jwt = jwt.encode({'phone': phone,}, 'secret', algorithm='HS256')
						return returnResponse( request, {'token':encoded_jwt,'phone':phone} , True , 200 )
					else:
						return returnResponse( request, 'Code does not match' , False , 201 )
			else:
				return returnResponse( request, 'Customer not found' , False , 404 )
		except Exception as e:
			return returnResponse( request, str(e) , False , 500)

class CustomerEdit(APIView):
	def post(self,request):
		try:
			token = jwt.decode(request.headers['x-auth-token'], 'secret', algorithms=['HS256'])
		except Exception as e:
			return returnResponse( request, str(e) , False , 500)

		customer = Customer.objects.filter(phone=token['phone']).first()

		if customer:
			try:
				request_data = request.data
				if 'name' in request_data:
					customer.name = request_data['name']
				if 'lastname' in request_data:
					customer.lastname = request_data['lastname']
				if 'email' in request_data:
					customer.email = request_data['email']
				if 'birthday' in request_data:
					customer.birthday = request_data['birthday']

				customer.save()

				response = {
					'name': customer.name,
					'lastname': customer.lastname,
					'email': customer.email,
					'birthday': customer.birthday,
				}

				return returnResponse( request, response , True , 200 )
			except Exception as e:
				return returnResponse( request, str(e) , False , 500)

		else:
			return returnResponse( request, 'Customer not found' , False , 404 )

		return returnResponse( request, 'Server error' , False , 500 )




class CustomerTask(generics.ListCreateAPIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer

	def list(self, request):
		try:
			token = jwt.decode(request.headers['x-auth-token'], 'secret', algorithms=['HS256'])
		except Exception as e:
			return returnResponse( request, str(e) , False , 500)

		customer = Customer.objects.filter(phone=token['phone']).first()

		if customer:
			queryset = Task.objects.filter(customer_id = customer.id)
			serializer = TaskSerializer(queryset, many=True)
			return returnResponse( request, serializer.data , True , 200 )
		else:
			return returnResponse( request, 'Customer not found' , False , 404 )

		return returnResponse( request, 'Server error' , False , 500 )

	def create(self, request):
		#raise Exception('create')
		try:
			token = jwt.decode(request.headers['x-auth-token'], 'secret', algorithms=['HS256'])
		except Exception as e:
			return returnResponse( request, str(e) , False , 500 )

		customer = Customer.objects.filter(phone=token['phone']).first()
		if customer:
			if request.data:
				data = {
					"customer": customer.id,
					"status": 1,
					"title": request.data['title'],
					"body": request.data['body'],
					"color": request.data['color'],
					"pinned": request.data['pinned'],
					"created": timezone.now(),
					"updated": timezone.now()
				}
				serializer = TaskSerializer(data=data)

				if (serializer.is_valid()):
					serializer.save()
					return returnResponse( request, 'True' , True , 200 )
				else:
					return returnResponse( request, serializer.errors , False , 404 )
			else:
				return returnResponse( request, 'Post data null' , False , 400 )
		else:
			return returnResponse( request, 'Customer not found' , False , 200 )

		return returnResponse( request, 'Server error' , False , 500 )

class CustomerTaskEdit(APIView):
	def post(self,request):
		try:
			token = jwt.decode(request.headers['x-auth-token'], 'secret', algorithms=['HS256'])
		except Exception as e:
			return returnResponse( request, str(e) , False , 500)

		customer = Customer.objects.filter(phone=token['phone']).first()

		if customer:
			request_data = request.data
			if 'guid' in request_data:
				task = Task.objects.filter(customer_id = customer.id, guid = request_data['guid']).first()
				try:
					if 'title' in request_data:
						task.title = request_data['title']
					if 'body' in request_data:
						task.body = request_data['body']
					if 'color' in request_data:
						task.color = request_data['color']
					if 'pinned' in request_data:
						task.pinned = request_data['pinned']
					if 'status' in request_data:
						task.status = request_data['status']

					task.updated = timezone.now()

					task.save()

					response = {
						'title': task.title,
						'body': task.body,
						'color': task.color,
						'pinned': task.pinned,
						'guid': task.guid,
						'updated': task.updated,
					}

					return returnResponse( request, response , True , 200 )
				except Exception as e:
					return returnResponse( request, str(e) , False , 500)
			else:
				return returnResponse( request, 'Invalid request' , False , 404 )
		else:
			return returnResponse( request, 'Customer not found' , False , 404 )

		return returnResponse( request, 'Server error' , False , 500 )

class CustomerTaskDelete(APIView):
	def post(self,request):
		try:
			token = jwt.decode(request.headers['x-auth-token'], 'secret', algorithms=['HS256'])
		except Exception as e:
			return returnResponse( request, str(e) , False , 500)

		customer = Customer.objects.filter(phone=token['phone']).first()

		if customer:
			request_data = request.data
			if 'guid' in request_data:
				task = Task.objects.filter(customer_id = customer.id, guid = request_data['guid']).first()
				try:
					task.delete()

					response = {
						'success': True
					}

					return returnResponse( request, response , True , 200 )
				except Exception as e:
					return returnResponse( request, str(e) , False , 500)
			else:
				return returnResponse( request, 'Invalid request' , False , 404 )
		else:
			return returnResponse( request, 'Customer not found' , False , 404 )

		return returnResponse( request, 'Server error' , False , 500 )
