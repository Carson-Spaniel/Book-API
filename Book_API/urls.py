from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookList.as_view(), name='apiList'),
    path('create/', views.BookCreate.as_view(), name='apiCreate'),
    path('find/<int:pk>/', views.Book.as_view(), name='apiFind'),
    path('edit/<int:pk>/<int:edit>/', views.Book.as_view(), name='apiEdit'),
]