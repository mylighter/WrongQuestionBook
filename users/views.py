from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from . import models

# Create your views here.


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            new_profile = models.UserProfile(user=new_user)
            authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('note:index'))
    return render(request, 'reg_and_login.html', context={
        'form': form, 'action': reverse('users:register'), 'tag': 'Register'
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('note:index'))


def ranking(request):
    ranking_list = models.UserProfile.objects.order_by('exp')
    return render(request, 'ranking.html', {'ranking_list': ranking_list})
