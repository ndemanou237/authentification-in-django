from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


def home(request):
    return render(request, 'app/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        nom_utilisateur = User.objects.create(username, email, password)
        nom_utilisateur.first_name = firstname
        nom_utilisateur.last_name = lastname
        nom_utilisateur.save()
        messages.success(request, 'votre compte à été crée avec success')
        return redirect('login')

    return render(request, 'app/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            firstname = user.firstname
            return render(request, 'app/index.html', {'firstname':firstname})

def logout(request):
    # return render(request, 'app/logout.html')    
    pass