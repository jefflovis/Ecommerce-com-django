from django.urls import path

from . import views

urlpatterns = [
	#Deixar como string vazia para url base    
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('create/', views.create, name="create"),
	path('painel/', views.painel, name="painel"),
	path('validation/', views.validation, name="validation"),
	path('dologin/', views.dologin, name="dologin"),
	

]