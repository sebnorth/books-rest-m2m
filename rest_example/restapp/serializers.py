from django.contrib.auth.models import User
from restapp.models import Book, Author

from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name')
        
class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer( many=True) 
    
    class Meta:
        model = Book
        fields = ('id', 'title', 'authors', 'user')
        #read_only_fields = ('id',)
    
    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)

        for author_data in authors_data:
            new_author, created = Author.objects.get_or_create(first_name=author_data['first_name'], last_name=author_data['last_name'])
            book.authors.add(new_author)
        return book   
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.user_id)
        authors_data = validated_data.pop('authors')
        for author_data in authors_data:
            new_author, created = Author.objects.get_or_create(first_name=author_data['first_name'], last_name=author_data['last_name'])
            instance.authors.add(new_author)
        instance.save()
        return instance
                 
class UserSerializer(serializers.ModelSerializer):
    books = BookSerializer(source='book_set', many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'books')



        


