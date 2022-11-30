from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import json
import datetime


from .models import *

# Create your views here.

def store(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Criando um carrinho vazio para usuários não logados
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
		cartItems = order['get_cart_items']
		
	products = Product.objects.all()
	context = {'products': products, 'cartItems': cartItems, 'items': items}
	return render(request, 'store/store.html', context)

def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
		cartItems = order['get_cart_items']

	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Criando um carrinho vazio para usuários não logados
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
		items = []
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems': cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action:', action)
	print('productId:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item adicionado', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
			)

	else:
		print('Usuário não está logado')
	return JsonResponse('Pagamento completo!', safe=False)


def create(request):
	return render(request, 'store/create.html')

def validation(request):
	data = {}
	if(request.POST['password'] != request.POST['password-conf']):
		data['msg'] = 'Senha e confirmação de Senha dferentes!'
		data['class'] = 'alert-danger'
	else:
		user = User.objects.create_user(request.POST['name'], request.POST['email'], request.POST['password'])
		user.first_name = request.POST['name']
		user.save()
		data['msg'] = 'Usuário cadastrado com sucesso!'
		data['class'] = 'alert-success'
	return render(request, 'store/create.html', data)

def painel(request):
	return render(request, 'store/painel.html')

def dologin(request):
	data = {}
	user = authenticate(username=request.POST['user'], password=request.POST['password'])
	if user is not None:
		login(request, user)
		data['msg'] = 'Login efetuado com sucesso!'
		data['class'] = 'alert-success'
		return render(request, 'store/painel.html', data)
	else:
		data['msg'] = 'Usuário ou Senha inválidos!'
		data['class'] = 'alert-danger'
		return render(request, 'store/painel.html', data)



	
