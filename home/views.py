from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
     peoples = [
          {'name':'sujana sharma','age':19},
          {'name':'srijana sharma','age':21},
           {'name':'sujan sharma','age':11},
    ]
     return render(request,"index.html",context={'peoples':peoples})

def success_page(request):
    return HttpResponse("hello this is a sucess page")