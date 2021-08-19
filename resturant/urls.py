from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'), #home page
    path('menu/', views.menu, name='menu'), #menu page
    path('menu/<str:pk>/details', views.menu_details, name="menu_details"),

    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name="logout"),
    path('profile/', views.userProfile, name="user_profile"),

    path('menu_adjustment/', views.adminMenuItem, name="admin_menu_item"),
    path('menu_adjustment/order/<str:pk>', views.orderDetails, name="order_details"),
    path('<str:pk>/details/delete/', views.delete_item, name="delete_item"),
    path('profile/password_change/', views.passwordChange, name='password_change'),
    path('<str:pk>/details/', views.adminMenuItemDetails, name='admin_detail'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="resturant/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="resturant/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="resturant/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="resturant/password_reset_done.html"),
         name="password_reset_complete"),

    path('cart/', views.cartView, name='cart'),
    path('cart/checkout/', views.checkoutView, name='checkout'),
    path('menu/update_item/', views.updateItem, name="update_item"),
    path('cart/update_item/', views.updateItem, name="update_item"),
    path('cart/checkout/update_delivery_info/', views.updateDeliveryInfo, name='update_delivery_info'),
    path('cart/checkout/process_order/', views.processOrder, name='process_order'),
    path('order_items_count/', views.orderCount, name='order_count'),
]
