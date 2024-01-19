from .models import BookObject
from .serializer import BookSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response
from django.urls import reverse
from django.db.models.functions import Lower

# Create your views here.

class BookList(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request):
        bookObjects = BookObject.objects.all().order_by(Lower('title'))

        # Getting search parameters
        searchQuery = request.query_params.get('search')
        perPage = request.query_params.get('perpage', default=2)

        # Filtering
        filter_conditions = Q()

        if searchQuery:
            filter_conditions |= Q(title__icontains=searchQuery) | Q(author__icontains=searchQuery)

        bookObjects = bookObjects.filter(filter_conditions)

        # Paginating
        paginator = PageNumberPagination()
        paginator.page_size = perPage

        result_page = paginator.paginate_queryset(bookObjects, request)

        # Serializing
        serializer = BookSerializer(result_page, many=True)

        total_pages = paginator.page.paginator.num_pages
        current_page = paginator.page.number

        # Get the base URL without any query parameters
        base_url = reverse('list')

        data = {
            'books': serializer.data,
            'total_pages': list(range(1, total_pages + 1)),
            'page_num': current_page,
            'page_range':total_pages,
            'next_link': f"{base_url}?{request.GET.urlencode()}&page={paginator.page.next_page_number()}" if paginator.page.has_next() else None,
            'prev_link': f"{base_url}?{request.GET.urlencode()}&page={paginator.page.previous_page_number()}" if paginator.page.has_previous() else None,
            'perpage': perPage,
        }

        return Response(data)
    
class BookCreate(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def post(self, request):
        title = request.data.get('title', [''])[0]
        author = request.data.get('author', [''])[0]
        pages = request.data.get('pages', [''])[0]

        data={
            'title':title.title(),
            'author':author.title(),
            'pages':pages
        }

        serializer = BookSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'book': serializer.data, 'pk': serializer.data['id'], 'created':True})
        else:
            return Response({'book': serializer.data, 'pk': serializer.data['id'], 'error':True})
        
class Book(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_book_by_pk(self, pk):
        bookObject = get_object_or_404(BookObject, pk=pk)
        return bookObject

    def get(self, request, pk):
        bookObject = self.get_book_by_pk(pk)
        serializer = BookSerializer(bookObject)
        return Response({'book': serializer.data, 'pk': pk})
    
    def post(self, request, pk, edit):
        title = request.data.get('title', [''])[0]
        author = request.data.get('author', [''])[0]
        pages = request.data.get('pages', [''])[0]

        data={
            'title':title.title(),
            'author':author.title(),
            'pages':pages
        }

        if edit:
            bookObject = self.get_book_by_pk(pk)
            serializer = BookSerializer(bookObject, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'book': serializer.data, 'pk': pk, 'saved':True})
            else:
                return Response({'book': serializer.data, 'pk': pk, 'error':True})
        else:
            bookObject = self.get_book_by_pk(pk)
            bookObject.delete()
            return Response({'detail':'book deleted'})