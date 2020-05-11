import json
from .models import *

#The purpose of this function is to handle 
# all the logic we created for our guest users order.

def cookieCart(request):
	#We want to find the logged user in users account, his order and his cart items.
    # This is of a user cart
 
    if request.user.is_authenticated:
        #then getting the customer along with finding or creating and order using the get_or_create() method
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        # Get the list of the orderitems for a given order
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items  #to query the cart item count.
    else:
        #Create an empty cart for the non logged in user
        #Get query cart/ cookies in view
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
            print('CART:',cart)
        items = []
        # We give them the value 0 for now 
        # We supposed that the cart is empty
        order = {'get_cart_total':0 , 'get_cart_items': 0}
        #let's query the order dictionary and also get the total by finding the key
        cartItems = order['get_cart_items']

        #Update our cart total
        #This loop will query the quantity of each item in our cart and 
        # add to the value of "cartItems" therefore giving us the total 
        # of all items + quantity in the entire cart.
        for i in cart:
            try:
                cartItems += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total': total,
                }
                items.append(item)
                
                if product.digital == False:
                    order['shipping'] = True
            except:
                pass
    return {'items' : items, 'order': order,'cartItems':cartItems}

def cartData(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']
	return {'items' : items, 'order': order,'cartItems':cartItems}

def guessOrder(request,data):
	name = data ['form']['name']
	email = data['form']['email']
	cookieData = cookieCart(request)
	items = cookieData['items']

    #Create customer and order
	customer,created = Customer.objects.get_or_create(email=email)
	customer.name = name
	customer.save()
        
	order = Order.objects.create(customer=customer, complete=False)

    #create items
	for item in items:
		product = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
                product = product,
                order = order,
                quantity = item['quantity'],
                
            )
	return customer,order