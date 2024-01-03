from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.book_list, name='list'),
]
