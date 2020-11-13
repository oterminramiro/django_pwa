from rest_framework import serializers
from .models import Status, Customer, CustomerCode

class StatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Status
		fields = ('name', 'key')


class CustomerSerializer(serializers.ModelSerializer):
	def validate(self, data):
		if len(str(data['phone'])) != 10 :
			raise serializers.ValidationError("phone must be valid")
		return data

	class Meta:
		model = Customer
		fields = ('name', 'lastname', 'phone', 'email', 'birthday', 'created', 'updated')

class CustomerCodeSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerCode
		fields = ('customer', 'code')
