from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookList.as_view(), name='list'),
    path('create/', views.BookCreate.as_view(), name='create'),
    path('<int:pk>/', views.Book.as_view(), name='find'),
    path('<int:pk>/<int:edit>/', views.Book.as_view(), name='edit'),
    path('<int:pk>/<int:delete>/', views.Book.as_view(), name='delete'),
]
