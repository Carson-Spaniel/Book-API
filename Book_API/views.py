from .models import BookObject
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import BookSerializer
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import status

# Create your views here.

# @api_view(['GET'])
# def book_list(request):
#     bookObjects = Book.objects.all()
#     serializer = BookSerializer(bookObjects, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# def book_create(request):
#     serializer = BookSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors)
    
# @api_view(['GET', 'PUT', 'DELETE'])
# def book(request, pk=None):
#     bookObject = get_object_or_404(Book, pk=pk)

#     if request.method == 'GET':
#         serializer = BookSerializer(bookObject)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         serializer = BookSerializer(bookObject, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method == 'DELETE':
#         bookObject.delete()
#         return Response(
#             {
#                 'detail': 'Book Deleted.'
#             }
#         )

class BookList(APIView):
    def get(self,request):
        bookObjects = BookObject.objects.all()
        serializer = BookSerializer(bookObjects, many=True)
        return Response(serializer.data)
    
class BookCreate(APIView):
    def get(self,request):
        return Response({
            'detail': 'Add a book to the list.'
        })
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class Book(APIView):
    def get_book_by_pk(self, pk):
        bookObject = get_object_or_404(BookObject, pk=pk)
        return bookObject

    def get(self, request, pk):
        bookObject = self.get_book_by_pk(pk)
        serializer = BookSerializer(bookObject)
        return Response(serializer.data)
    
    def put(self, request, pk):
        bookObject = self.get_book_by_pk(pk)
        serializer = BookSerializer(bookObject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        bookObject = self.get_book_by_pk(pk)
        bookObject.delete()
        return Response(
            {
                'detail': 'Book Deleted.'
            }
        )