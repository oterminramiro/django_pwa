from django.urls import path

from . import views

urlpatterns = [
	path("customer_list/", views.CustomerList.as_view(), name="customer_list"),
	path("customer_exist/<int:phone>/", views.CustomerExist.as_view(), name="customer_exist"),
	path("customer_code/", views.CustomerCode.as_view(), name="customer_code"),
	path("customer_login/", views.CustomerLogin.as_view(), name="customer_login"),
	path("customer_edit/", views.CustomerEdit.as_view(), name="customer_edit"),

	path("customer_task/", views.CustomerTask.as_view(), name="customer_task"),
]
