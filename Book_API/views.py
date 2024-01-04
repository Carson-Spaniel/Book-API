from .models import BookObject
from rest_framework.response import Response
from .serializer import BookSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage

# Create your views here.

class BookList(APIView):
    def get(self,request):
        bookObjects = BookObject.objects.all()
        search = request.query_params.get('search')
        perPage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)

        if search:
            bookObjects = bookObjects.filter(title__icontains=search)

        paginator = Paginator(bookObjects, per_page=perPage)
        try:
            bookObjects = paginator.page(number=page)
        except EmptyPage:
            bookObjects = []

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