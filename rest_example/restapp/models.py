from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
 
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
 
class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    user = models.ForeignKey(User)
 
    def __str__(self):
        return self.title
        

