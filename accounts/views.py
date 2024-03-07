from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    context_object_name = 'form'
    success_url = reverse_lazy('login')


def logout_view(request):
    logout(request)
    return redirect('home')
