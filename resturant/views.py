from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import *
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
import json, datetime
from .utils import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def orderCount(request):
    data = json.loads(request.body)

    if request.user.is_authenticated:
        order = request.user.customer.order_set.get(status="Order In Progress")
        itemCount = {"item_count": order.get_cart_items}
    else:
        cookieTotal = 0

        for i in data:
            cookieTotal += int(data[str(i)]['quantity'])

        itemCount={'item_count' : cookieTotal}

    return JsonResponse(itemCount)


def orderDetails(request, pk):
    currentOrder = Order.objects.get(id=pk)
    orderItems = currentOrder.orderitem_set.all()

    try:
        shippingAddress = currentOrder.customer.shippingaddress
    except:
        shippingAddress = "Customer has no shipping address"

    form = OrderForm(instance=currentOrder)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=currentOrder)
        if form.is_valid():
            form.save()
            return redirect("admin_menu_item")

    context = {
     "form" : form,
     "order" : currentOrder,
     "order_items" : orderItems,
     "shipping_address" : shippingAddress,
    }
    return render(request, 'resturant/order_details.html', context)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp();
    data = json.loads(request.body)

    print(data)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status="Order In Progress")
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.status = "Order Confirmed"
    order.save()

    if order.pickup == False:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse("Hello", safe=False)

def updateDeliveryInfo(request):
    data = json.loads(request.body)

    checkValue = data['buttonChecked']
    orderId = data['orderId']

    if(orderId):
        currentOrder = Order.objects.get(id=orderId)

        if(checkValue=="pickup"):
            currentOrder.pickup = True
        else:
            currentOrder.pickup = False

        currentOrder.save()

    return JsonResponse("Request Successful", safe=False);

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = MenuItem.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, status="Order In Progress")
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False);

def checkoutView(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items' : items,
        'order' : order,
        'cart-items': cartItems,
    }
    return render(request, 'resturant/checkout.html', context)

def cartView(request):
    try:
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
    except:
        pass
    context = {
        'items' : items,
        'order' : order,
        'cart-items' : cartItems,
    }
    return render(request, 'resturant/cart.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminMenuItemDetails(request, pk):
    currentItem = MenuItem.objects.get(id=pk)
    form = AddMenuItem(instance=currentItem)
    if request.method == 'POST':
        form = AddMenuItem(request.POST, request.FILES, instance=currentItem)
        if form.is_valid():
            user = form.save()
            return redirect('admin_menu_item')
        else:
            print(form.errors)

    context = {
        'form': form,
        'item': currentItem,
    }
    return render(request, 'resturant/menu_items_details_admin.html', context)


@login_required(login_url='login')
def passwordChange(request):
    errorList=[]
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')

            return redirect('user_profile')
        else:
            print(form.errors)
            for key, value in form.errors.items():
                errorList.append(value)
    else:
        form = PasswordChangeForm(user=request.user)

    context = {
        'form' : form,
        'errors' : errorList,
    }

    return render(request, 'resturant/password_change.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_item(request, pk):
    seletedItem = MenuItem.objects.get(id=pk)

    if request.method == "POST":
        seletedItem.delete()
        return redirect('admin_menu_item')

    context = {
        'item': seletedItem,
    }

    return render(request, 'resturant/delete_item.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userProfile(request):
    currentUser = request.user.customer
    form = CustomerSettingUpdateForm(instance=currentUser)
    if request.method == "POST":
        form = CustomerSettingUpdateForm(request.POST, request.FILES, instance=currentUser)
        if form.is_valid():
            form.save()


    context = {
        'current_user' : currentUser,
        'form' : form,
    }
    return render(request, 'resturant/user_profile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminMenuItem(request):
    #form handling
    items = MenuItem.objects.all()
    form = AddMenuItem()
    confirmedOrders = Order.objects.filter(status="Order Confirmed")
    beingDeliveredOrders = Order.objects.filter(status="Out for delivery")


    if request.method =="POST":
        form = AddMenuItem(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_menu_item')

    context = {
        'items': items,
        'form': form,
        'confirmed_orders': confirmedOrders,
        'orders_being_delivered' : beingDeliveredOrders,
    }
    return render(request, 'resturant/admin_menu_item.html', context)


def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={
        "cartItems": cartItems,
    }
    return render(request, 'resturant/home.html', context)

def menu(request):

    fries = MenuItem.objects.filter(item_type="fries")
    entrees = MenuItem.objects.filter(item_type="entree")
    aioliSauces = MenuItem.objects.filter(sauce_type="aioli")
    ketchupSauces = MenuItem.objects.filter(sauce_type="ketchup")
    context = {
        "fries": fries,
        "entrees" : entrees,
        "aioli_sauces" : aioliSauces,
        "ketchup_sauces" : ketchupSauces,
    }
    return render(request, 'resturant/menu.html', context)

def menu_details(request, pk):
    #add a try catch to get the 404 on an object not found
    menu_item_name = MenuItem.objects.get(id=pk)
    context = {
        "menu_item_name": menu_item_name,
    }
    return render(request, 'resturant/menu_item_details.html', context)

@unaunthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
        else:
            messages.info(request, "Username or Password is incorrect")

    context = {
    }
    return render(request, 'resturant/login.html', context)

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('home')

@unaunthenticated_user
def registerPage(request):
    customerGroup = Group.objects.get(name="customer")

    form = CreateUserForm()
    errorList = []
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            """
            This was used before siganls
            newUser = User.objects.get(username=form.cleaned_data.get('username'))
            customerGroup.user_set.add(newUser)
            email = form.cleaned_data.get('email')

            newCustomer = Customer.objects.create(user=user, name="", email=email, phone='')
            """

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        else:
            for key, value in form.errors.items():
                errorList.append(value)

    context = {
        'form' : form,
        'errors' : errorList,
    }
    return render(request, 'resturant/register.html', context)
