from rest_framework import serializers
from .models import BookObject

class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    author = serializers.CharField()
    pages = serializers.IntegerField()

    def create(self, data):
        return BookObject.objects.create(**data)
    
    def update(self, instance, data):
        instance.title = data.get('title', instance.title)
        instance.author = data.get('author', instance.author)
        instance.pages = data.get('pages', instance.pages)

        instance.save()
        return instance