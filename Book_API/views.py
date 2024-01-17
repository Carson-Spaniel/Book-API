from .models import BookObject
from .serializer import BookSerializer
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.views.generic import TemplateView

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

# Create your views here.

class Login(TemplateView):
    def get(self, request):
        return render(request, 'login.html') 

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

class BookList(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self,request):
        bookObjects = BookObject.objects.all().order_by('title')

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

        return render(request, 'books.html', {
            'books': serializer.data,
            'total_pages': range(1, total_pages + 1),
            'next_link': paginator.get_next_link(),
            'prev_link': paginator.get_previous_link(),
            'perpage': perPage,
        })
    
class BookCreate(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self,request):
        return render(request, 'createBook.html')
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return render(request, 'editBook.html', {'book': serializer.data, 'pk': serializer.data['id'], 'created':True})
        else:
            return render(request, 'editBook.html', {'book': serializer.data, 'pk': serializer.data['id'], 'error':True})
        
class Book(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_book_by_pk(self, pk):
        bookObject = get_object_or_404(BookObject, pk=pk)
        return bookObject

    def get(self, request, pk):
        bookObject = self.get_book_by_pk(pk)
        serializer = BookSerializer(bookObject)
        return render(request, 'editBook.html', {'book': serializer.data, 'pk': pk})
    
    def post(self, request, pk, edit):
        if edit:
            bookObject = self.get_book_by_pk(pk)
            serializer = BookSerializer(bookObject, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return render(request, 'editBook.html', {'book': serializer.data, 'pk': pk, 'saved':True})
            else:
                return render(request, 'editBook.html', {'book': serializer.data, 'pk': pk, 'error':True})
        else:
            bookObject = self.get_book_by_pk(pk)
            bookObject.delete()
            return redirect('/books')