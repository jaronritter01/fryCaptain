from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
# Create your models here.

class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

class MenuItem(models.Model):
    ITEMTYPE = (
                ('fries','fries'),
                ('entree', 'entree'),
                ('dessert', 'dessert'),
                ('sauce', 'sauce'),
                )
    SAUCETYPE = (
            ('aioli','aioli'),
            ('ketchup', 'ketchup'),
    )
    name = models.CharField(max_length = 50, null=True)
    sauce_type = models.CharField(max_length=200, null=True, blank=True, choices=SAUCETYPE)
    description = models.TextField(max_length = 250, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    item_type = models.CharField(max_length=200, null=True, choices=ITEMTYPE)
    date_created = models.DateTimeField(auto_now_add = True, null=True)
    item_pic = models.ImageField(default='solid-dark-grey-background.jpg',null=True, blank=True)

    def __str__(self):
        return self.name;

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50, null=True)
    email = models.CharField(max_length = 100, null=True)
    phone = models.CharField(max_length = 15, null=True)
    profile_pic = models.ImageField(default='defaultProfilePic.png',null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add = True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
            ('Order In Progress', 'Order In Progress'),
            ('Order Confirmed', 'Order Confirmed'),
            ('Out for delivery', 'Out for delivery'),
            ('Arrived', 'Arrived'),
            )

    pickup = models.BooleanField(default=False, null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add = True, null=True)
    status = models.CharField(max_length=200, null=True, choices = STATUS)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return self.customer.name + "'s order with id: " + str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
