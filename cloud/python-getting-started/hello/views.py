from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')

    # Put custom Python code here! http://stackoverflow.com/questions/29464285/run-python-script-from-parse-cloud-code-background-job


    # Import ParsePy stuff. ParsePy makes using Parse in Python much easier.
    from parse_rest.connection import ParseBatcher, register#, SessionToken
    from parse_rest.datatypes import Function, Object#, ACL
    #from parse_rest.role import Role
    from parse_rest.user import User
    # Calling "register" allows parse_rest / ParsePy to work.
    # - register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
    register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
             "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
             master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
             )

    # Create a simple "Event" object in Parse
    class Event(Object):
        pass
    e = Event()
    e.score = 10
    e.save()
    print("Event's score is {}. What's good, yo?!".format(e.score))

    try:
        import update_in_Parse
        update_in_Parse.main()
        print("update_in_Parse worked!")
    except:
        print("update_in_Parse didn't work.")




    return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

