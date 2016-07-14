from django.contrib.auth.models import User
from restapp.models import Book, Author
from restapp.forms import UserForm
from restapp.serializers import  AuthorSerializer, BookSerializer,  UserSerializer

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


class AuthorViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing author instances.
    """
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing author instances.
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    
class UserList(APIView):
    """
    List all users, or create a new user.
    """
    permission_classes =(IsAdminUser, )
    #authentication_classes = (JSONWebTokenAuthentication, )
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
           
class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    permission_classes =(IsAuthenticated, )
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):   
        if int(pk)==request.user.id or request.user.is_staff:  
            user = self.get_object(pk)
            user = UserSerializer(user)
            return Response(user.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    
    else:
        user_form = UserForm()

    return render_to_response(
            'register.html',
            {'user_form': user_form, 'registered': registered},
            context)


def user_login(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/users/'+str(user.id)+'/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render_to_response('registration/login.html', {}, context)



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
