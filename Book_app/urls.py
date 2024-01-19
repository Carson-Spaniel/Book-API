from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookList.as_view(), name='list'),
    path('create/', views.BookCreate.as_view(), name='create'),
    path('login/', views.Login.as_view(), name='login'),
    path('<int:pk>/', views.Book.as_view(), name='find'),
    path('<int:pk>/<int:edit>/', views.Book.as_view(), name='edit'),
    path('<int:pk>/<int:delete>/', views.Book.as_view(), name='delete'),
]

handler404 = 'Book_app.views.handler404'
handler500 = 'Book_app.views.handler500'