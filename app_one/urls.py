from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout',views.logout),
    path('dashboard', views.dashboard),
    path('add_item', views.add_item),
    path('create_item', views.create_item),
    path('add_wish', views.add_wish),
    path('remove_wish/<int:id>/', views.remove_wish),
    path('delete_wish/<int:id>/', views.delete_wish),
    path('show_item/<int:id>/', views.show_item),
]