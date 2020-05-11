from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Along with a User model each customer will contain 
# a Customer model that holds a one to one relationship to each user

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=200)
    
    #The representation of the model customer in the database
    def __str__(self):
        return self.name
    
#The product model represents products we have in store.
class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(default=0)
    #To check if it's physical or digital in order to be shipped or not
    digital =  models.BooleanField(default=False, blank=True, null=True) 
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

    #We want to add an imageURL method to either render an image 
    #or an empty string so we don't get an error in the front end

    # Return the function of the class as an attribute 
    @property 
    def imageURL(self):
        try:
            url = self.image.url 
        except:
            url = ''
        return url


#The order model will represent a transaction that is placed or pending. 
# The model will hold information such as the transaction ID, 
# data completed and order status. 
# This model will be a child or the customer model but a parent to Order Items.

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
    
    #we need to create a method to check if we have
    # any items which are not digital
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

    #We want to get the total price for the all items
	def get_cart_total(self):
		orderitems = self.orderitem_set.all() # Grab all the items choosen
		total = sum([item.get_total for item in orderitems]) #Calculate total price
		return total 

    #we want get the quantity in total 
	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all() # Grab all the items choosen
		total = sum([item.quantity for item in orderitems]) # Calculate the total of quantity
		return total 




#An order Item is one item with an order. So for example a shopping cart may consist of many items
# but is all part of one order. Therefore the OrderItem model 
# will be a child of the PRODUCT model AND the ORDER Model.
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    # We want to get the total price for an order item
    # depending on the quantity given
    def get_total(self):
        total = self.product.price * self.quantity
        return total




#Not every order will need shipping information. 
# For orders containing physical products that need to be shipped
# we will need to create an instance of the shipping model 
# to know where to send the order. 
# Shipping will simply be a child of the order model when necessary.

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address