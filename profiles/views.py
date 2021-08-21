from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from profiles.forms import SignUpForm
from django.contrib import messages
# Create your views here.




class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('profiles:login')
    template_name = 'profiles/signup.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f"Your Account has been created successfully")
        return super(SignUpView, self).form_valid(form)


