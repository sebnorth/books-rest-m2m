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
    books = BookSerializer(source='book_set', many=True, required=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'books')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

        


    
        


