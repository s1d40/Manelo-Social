from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views import View
from .models import ManeloUser
from .forms import UserRegistrationForm, CustomAuthenticationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

# Create your views here.


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'core/login.html'  # Update with your template path

    def form_valid(self, form):
        # Call the base class form_valid to perform standard authentication
        super().form_valid(form)
        # Check if 'remember_me' is checked
        if form.cleaned_data.get('remember_me'):
            # Set session expiry to 2 weeks if 'remember_me' is true
            self.request.session.set_expiry(1209600)  # 2 weeks in seconds
        else:
            # Session expires when the user closes the browser
            self.request.session.set_expiry(0)
        # Redirect the user to a specified URL after successful login
        # Redirect to the home page with the user's primary key (pk) as part of the URL
        return redirect(reverse('home', kwargs={'pk': self.request.user.pk}))  # Updated to include user's pk in the redirect URL

    
 
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Custom logic here
        # For example, you could log a message, clear some session data, etc.
        response = super().dispatch(request, *args, **kwargs)
        return response
 
 
class HomeView(DetailView):
    
    model = ManeloUser
    template_name = 'core/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["object"] = self.request.user
        return context



def HomeRedirect(request):
    if request.user.is_authenticated:
        return redirect(reverse('home', kwargs={'pk': request.user.pk})) 
    else: return redirect(reverse('login'))
    

class UserRegister(CreateView):
    
    template_name = 'core/signup.html'
    success_url = reverse_lazy('login')
    form_class = UserRegistrationForm
    success_message = 'Profile created successfully'
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.user = self.request.user
        # Handle file upload here if necessary
        return super().form_valid(form)