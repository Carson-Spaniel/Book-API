from django.shortcuts import render
from .models import Book
from django.http import JsonResponse

# Create your views here.
def book_list(request):
    bookObjects = Book.objects.all()
    books = list(bookObjects.values())

    return JsonResponse({
        'books': books
    })