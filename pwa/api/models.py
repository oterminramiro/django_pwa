from django.db import models
from django.utils import timezone
import uuid

class Status(models.Model):
	name = models.CharField(max_length=100)
	key = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Customer(models.Model):
	name = models.CharField(max_length=100, null=True)
	lastname = models.CharField(max_length=100, null=True)
	phone = models.CharField(unique=True,max_length=100)
	email = models.CharField(unique=True,max_length=100, null=True)
	birthday = models.DateField(null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

class CustomerCode(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
	code = models.CharField(max_length=6)

class TaskStatus(models.Model):
	name = models.CharField(max_length=100)
	key = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Task(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
	status = models.ForeignKey(TaskStatus, on_delete=models.PROTECT)
	title = models.CharField(max_length=100, null=True)
	body = models.CharField(max_length=300)
	color = models.CharField(max_length=100)
	pinned = models.BooleanField()
	guid = models.UUIDField(default=uuid.uuid4, editable=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
