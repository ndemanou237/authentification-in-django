from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from authentification import settings
from django.core.mail import send_mail


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
        if User.objects.filter(username=username):
            messages.error(request, "ce nom d'utilisateur existe déjà")
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request, 'cet email est deje lié a un utilisateur')
            return redirect('register')
        if not username.isalnum():
            messages.error(request, 'le nom doit être alphanumérique')   
            return redirect('register') 
        if password != password1:
            messages.error(request, 'les deux mots de passe ne sont pas identique')



        nom_utilisateur = User.objects.create_user(username, email, password)
        nom_utilisateur.first_name = firstname
        nom_utilisateur.last_name = lastname
        nom_utilisateur.save()
        messages.success(request, 'votre compte à été crée avec success')
        subject = "bienvenue sur authentification system"
        message = "Bienvenue" + nom_utilisateur.first_name + " " + nom_utilisateur.last_name + "\n Nous sommes heureux de vous compter parmi nous\n\n\n Merci \n\n Donald"
        from_email = settings.EMAIL_HOST_USER
        to_list = [nom_utilisateur.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        return redirect('login')

    return render(request, 'app/register.html')

def logIn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            firstname = user.first_name
            context = {
                'firstname': user

            }
            print(user)
            return render(request, 'app/index.html', context)
        else:
            messages.error(request, 'Mauvaise authentification')
            return redirect('login')
    return render(request, 'app/login.html')    

def logOut(request):
    logout(request)
    messages.success(request, 'vous avez été bien déconnecté')
    return redirect('home')