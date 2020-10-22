from .models import Book, Genre
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(read_only=True, view_name='author-detail')

    class Meta:
        model = Book
        fields = ['url', 'title', 'author', 'summary', 'isbn', 'genre']

    
