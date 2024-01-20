from .models import BookObject
from .serializer import BookSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import View, APIView
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.urls import reverse
from django.db.models.functions import Lower
from django.http import JsonResponse

# Create your views here.

class BookList(View):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request):
        bookObjects = BookObject.objects.all().order_by(Lower('title'))

        # Getting search parameters
        searchQuery = request.GET.get('search')
        perPage = request.GET.get('perpage', default=2)

        # Filtering
        filterConditions = Q()

        if searchQuery:
            filterConditions |= Q(title__icontains=searchQuery) | Q(author__icontains=searchQuery)

        bookObjects = bookObjects.filter(filterConditions)

        # Paginating
        paginator = Paginator(bookObjects, perPage)

        pageNumber = request.GET.get('page', 1)
        resultPage = paginator.get_page(pageNumber)

        # Serializing
        serializer = BookSerializer(resultPage, many=True)

        total_pages = paginator.num_pages

        data = {
            'books': serializer.data,
            'total_pages': list(range(1, total_pages + 1)),
            'page_num': resultPage.number,
            'page_range': total_pages,
            'next_link': f"{reverse('list')}?{request.GET.urlencode()}&page={resultPage.next_page_number()}" if resultPage.has_next() else None,
            'prev_link': f"{reverse('list')}?{request.GET.urlencode()}&page={resultPage.previous_page_number()}" if resultPage.has_previous() else None,
            'perpage': perPage,
        }

        return JsonResponse(data)
    
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
            return JsonResponse({'book': serializer.data, 'pk': serializer.data['id'], 'created':True})
        else:
            return JsonResponse({'book': serializer.data, 'pk': serializer.data['id'], 'error':True})
        
class Book(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_book_by_pk(self, pk):
        bookObject = get_object_or_404(BookObject, pk=pk)
        return bookObject

    def get(self, request, pk):
        bookObject = self.get_book_by_pk(pk)
        serializer = BookSerializer(bookObject)
        return JsonResponse({'book': serializer.data, 'pk': pk})
    
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
                return JsonResponse({'book': serializer.data, 'pk': pk, 'saved':True})
            else:
                return JsonResponse({'book': serializer.data, 'pk': pk, 'error':True})
        else:
            bookObject = self.get_book_by_pk(pk)
            bookObject.delete()
            return JsonResponse({'detail':'book deleted'})