# books-rest-m2m

## Aplikacja tworzy REST API dla CRUD-a dla następującej logiki:

- Użytkownik posiada listę ulubionych książek, 
- Książka z Autorem jest relacją typu Many2Many

### Instalacja

cd C:\Users\sebnorth\workspace\django\roboczy

git clone https://github.com/sebnorth/books-rest-m2m.git

C:\Python34\python -m venv myvenv

myvenv\Scripts\activate

pip install Django==1.9.7 PyJWT==1.4.0 djangorestframework==3.3.3 djangorestframework-jwt==1.8.0

cd books-rest-m2m\rest_example\

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

np.: user: sebnorth pwd: sebnorth email: admin@admin.com

python manage.py runserver

http://127.0.0.1:8000/

### Obłsuga aplikacji

Na początku trzeba się zalogować supersuerem albo wejść na http://127.0.0.1:8000/register i się zarejestrować a następnie zalogować. 

http://127.0.0.1:8000/users/ widzi tylko osoba z permission_classes =(IsAdminUser, )
dlatego proponuję na początek zalogować się supersuerem. 

#### przykładowe dane: 

{
  "first_name": "Charles",
  "last_name": "Wheeler",
  "email": "cwheeler0@oracle.com",
  "username": "cwheeler0",
  "password": "au3s9SfAsQN"
}, 

{
  "first_name": "Joe",
  "last_name": "Williams",
  "email": "jwilliams1@ezinearticles.com",
  "username": "jwilliams1",
  "password": "4cVcIV"
}, 

{
  "first_name": "Terry",
  "last_name": "Webb",
  "email": "twebb2@typepad.com",
  "username": "twebb2",
  "password": "R1FgrjWVLMV9"
}, 

{
  "first_name": "Andrew",
  "last_name": "Webb",
  "email": "awebb3@google.com.br",
  "username": "awebb3",
  "password": "30WbIsVwO1bz"
}, 

{
  "first_name": "Phyllis",
  "last_name": "Rogers",
  "email": "progers4@posterous.com",
  "username": "progers4",
  "password": "3NupG2"
}

### Przykładowe aktywności: 

1. Dodamy użytkownika cwheeler0 z listy powyżej

  w http://127.0.0.1:8000/users/ w pole content wpisujemy: 
  
  {
    "first_name": "Charles",
    "last_name": "Wheeler",
    "email": "cwheeler0@oracle.com",
    "username": "cwheeler0",
    "password": "au3s9SfAsQN"
  }
  
  i zatwierdzamy przyciskiem POST, następnie odświeżamy http://127.0.0.1:8000/users/
  
  Użytkownik cwheeler0 będzie miał id=2 jeśli wcześniej nie tworzyliśmy żadnego użytkownika, będzie miał dostęp po zalogowaniu tylko do widoku  http://127.0.0.1:8000/users/2/

2. W tym widoku zrobimy PUT:

{
"last_name": "Wheeler123",
"username": "cwheeler0",
"password": "au3s9SfAsQN"
}


3. Dodamy paru autorów i parę książek

"authors": "http://127.0.0.1:8000/authors/",

"books": "http://127.0.0.1:8000/books/"

Autorzy:

{"first_name": "Robert","last_name": "Lewandowski"}

{"first_name": "Kuba","last_name": "Błaszczykowski"}

{"first_name": "Arkadiusz","last_name": "Milik"}

Książki

{
    "title": "Euro 2016",
    "authors": [{"first_name": "Robert","last_name": "Lewandowski"}],
    "user": 1
}

{
    "title": "Moje gole",
    "authors": [{"first_name": "Kuba","last_name": "Błaszczykowski"}],
    "user": 1
}


{
    "title": "Jak pokonaliśmy Szwajcarię.",
    "authors": [{"first_name": "Robert","last_name": "Lewandowski"}, {"first_name": "Arkadiusz","last_name": "Milik"}],
    "user": 2
}

Książki i autorów może dodawać każdy zalogowany użytkownik('DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',))

4. Dla zalogowanego superusera w widoku UserList można odkomentować #authentication_classes = (JSONWebTokenAuthentication, ), następnie uzyskać token: http://127.0.0.1:8000/api-token-auth/

i z konsoli wykonać coś w stylu:

curl.exe -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IiIsInVzZXJuYW1lIjoiTHVkd2lrIiwidXNlcl9pZCI6NiwiZXhwIjoxNDY4NDUyMDk2fQ.XWUknceOtruPHyq7C5fpnE3ffWbPu9HbK5iBglBg2js" http://127.0.0.1:8000/users/
