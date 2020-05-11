from django.shortcuts import render
from django.http import JsonResponse
from .models import * 
import datetime
import json
from .utils import cookieCart, cartData, guessOrder
# Create your views here.

# This is the store view 
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all() # We want to query all the products from the store
    context = {'products' : products,'cartItems':cartItems}
    return render(request,'store/store.html',context)

# This is the cart view 
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items' : items, 'order': order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)

# This is the checkout view 
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items' : items, 'order': order,'cartItems':cartItems, 'shipping': False}
    return render(request,'store/checkout.html',context)


# We want to send the product.id along with an action of "add" or "remove" to
# the view we are about to create
# So we will send the return value (the data) in a simple Jsonresponse
def updateItem(request):
    # we want to set the action and productId variables by accessing the data variable.
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    #Create OR Update Order & OrderItem
    #We are going to use the product id to query the product and use 
    # "get_or_create" in order to work with the status: 
    # "False", because the complete attribute means it's an open cart we can add to.
    customer = request.user.customer 
    product = Product.objects.get(id=productId) # We get the product of the specific user 
    order, created = Order.objects.get_or_create(customer=customer, complete=False) 

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) 
    
    # we want to add in some logic to update or remove an item from our order
    if action == 'add':
	    orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
	    orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    #if the quantity is at or below zero,
    #if so we want to simply remove this item from the cart.
    if orderItem.quantity <= 0:
	    orderItem.delete()

    return JsonResponse('Item was added',safe=False)

#let's first create our "view" to process order
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp() # We want to create a transaction id
    data = json.loads(request.body)

    #Now we want to parse the data sent from the post request and query/create 
    # some data if a user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer,order = guessOrder(request,data)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

        #we will be sending the total from the frontend, 
        # we want to make sure that the total sent matches 
        # what the cart total is actually supposed to be.

    if total == order.get_cart_total:
        order.complete = True
    order.save()

     #we need to create an instance of the shipping address if an address was sent
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order ,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
    return JsonResponse('Payment submitted...', safe=False)

