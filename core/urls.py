from django.urls import path
from .import views
from user import views as user_view 
from pine import views as pine_view 
from chat import views as chat_view

urlpatterns = [
    path('', views.main, name="home"),
    path('index/', views.index, name="index"),
    path('expenses/', views.expenses, name="expenses"),
    path('revenues/', views.revenues, name="revenues"),
    path('workers_pay/', views.workers_pay, name="workers_pay"),

    path('register/', user_view.user_register, name="register"),
    path('login/', user_view.user_login, name="login"),
    path('logout/', user_view.user_logout, name="logout"),
    path('activate/<uidb64>/<token>', user_view.activate, name="activate"),
    path('pine_prices/', views.pine_price_list, name='pine_price_list'),


    path('list_user/', views.user_list, name="list-user"),
    path('user_delete/<int:pk>/', views.user_delete, name="user_delete"),
    path('employee/', views.employee, name="empl-page"),
    path('supplier/', views.supplier, name="sup-page"),
    path('buyer/', views.buyer, name="buy-page"),

    path('crop/', pine_view.crop, name="crop"),
    path('category/', pine_view.category, name="category"),
    path('cat_delete/<int:pk>/', pine_view.cat_delete, name="cat_delete"),
    path('crop_delete/<int:pk>/', pine_view.crop_delete, name="crop_delete"),
    path('crop_update/<int:pk>/', pine_view.crop_update, name='crop_update'),
    path('price/', views.price, name='price'),
    path('price_edit/<int:pk>/', views.edit_price, name='price_edit'),
    path('edit_value/<int:pk>/', views.edit_value, name='edit_value'),
    path('edit_price/<int:pk>/', views.edit_price, name='edit_price'),
    path('yield/', pine_view.yields, name="yield"),
    path('yield_delete/<int:pk>/', pine_view.yield_delete, name="yield_delete"),
    path('yield_update/<int:pk>/', pine_view.yield_update, name='yield_update'),

    # path('bad_pine/', pine_view.pine_bad, name="bad_pine"),
    # path('bad_pine_update/<int:pk>/', pine_view.bad_pine_update, name='bad_pine_update'),

    path('rooms/', chat_view.rooms, name="rooms"),
    path('bidding/', chat_view.bidding, name="bidding"),
    path('bidder_win_list/', chat_view.bidder_win_list, name="bidder_win_list"),
    path('room/<slug:slug>/', chat_view.room, name="room"),
    path('room_delete/<int:pk>/', chat_view.room_delete, name='room_delete'),

    path('notifications/', views.all_notifications, name='all_notifications'),
]