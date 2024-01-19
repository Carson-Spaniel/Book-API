from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
import requests
from urllib.parse import urljoin
from django.middleware.csrf import get_token
import json
from django.conf import settings
import os

TEMPLATE_DIRS = [
    os.path.join(settings.BASE_DIR, "templates"),
]

# Create your views here.

def index(request):
    return redirect(reverse('login'))

def get_api_data(http_method, url, data=None, request=None):
    if http_method == 'GET':
        response = requests.get(url)
    elif http_method == 'POST':
        csrf_token = get_token(request)
        headers={
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        }
        response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

class Login(TemplateView):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        print(request.POST)
        return redirect(reverse('list'))

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

class BookList(TemplateView):
    def get(self,request):
        host_url = f'http://{request.get_host()}'
        apiUrl = reverse('apiList')
        full_url = urljoin(host_url, apiUrl+ '?' + '&'.join([f'{key}={value}' for key, value in request.GET.items()]))
        apiData = get_api_data('GET', full_url)
        return render(request, 'books.html', apiData)
    
class BookCreate(TemplateView):
    def get(self,request):
        return render(request, 'createBook.html')
    
    def post(self, request):
        host_url = f'http://{request.get_host()}'
        apiUrl = reverse('apiCreate')
        full_url = urljoin(host_url, apiUrl)
        apiData = get_api_data('POST', full_url, json.dumps(dict(request.POST)), request=request)
        return render(request, 'editBook.html', apiData)
        
class Book(TemplateView):
    def get(self, request, pk):
        host_url = f'http://{request.get_host()}'
        apiUrl = reverse('apiFind', kwargs={'pk': pk})
        full_url = urljoin(host_url, apiUrl)
        apiData = get_api_data('GET', full_url)
        return render(request, 'editBook.html', apiData)
    
    def post(self, request, pk, edit):
        apiUrl = reverse('apiEdit', kwargs={'pk': pk, 'edit': edit})
        if edit:
            host_url = f'http://{request.get_host()}'
            full_url = urljoin(host_url, apiUrl)
            apiData = get_api_data('POST', full_url, json.dumps(dict(request.POST)), request=request)
            return render(request, 'editBook.html', apiData)
        else:
            host_url = f'http://{request.get_host()}'
            full_url = urljoin(host_url, apiUrl)
            apiData = get_api_data('POST', full_url, request=request)
            return redirect('/books')
