from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.
def login(request):

    return redirect('login')

def logout(request):
    logout(request)
    
    print('sdsdsdssdsdd')
    return redirect('logout')

