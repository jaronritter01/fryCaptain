import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'pickup': False}
    cartItems = order['get_cart_items']

    for i in cart:
        cartItems += cart[i]['quantity']

        product = MenuItem.objects.get(id=i)
        total = (product.price * cart[i]['quantity'])

        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]['quantity']

        item = {
            'product':{
                'id': product.id,
                'name' : product.name,
                'price' : product.price,
                'item_pic' : product.item_pic,
            },
            'quantity' : cart[i]['quantity'],
            'get_total' : total,
        }

        items.append(item)
    return {'cartItems' : cartItems, 'order':order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status="Order In Progress")
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']


    return {'cartItems' : cartItems, 'order':order, 'items': items}

def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,

    )
    customer.name = name
    customer.save()

    Order.objects.create(
        customer = customer,
        status = "Order In Progress",
    )

    for item in items:
        product = MenuItems.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity'],
        )

        return customer, order
