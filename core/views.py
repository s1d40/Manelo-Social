from typing import Any
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views import View
from .models import ManeloUser, ChatRoom, Message
from .forms import UserRegistrationForm, CustomAuthenticationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .serializers import ChatRoomSerializer, MessageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

# Create your views here.



def chat_room(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    return render(request, 'chat_room.html', {'chat_room': chat_room})


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Example of filtering by sender or recipient
        if 'sender' in self.request.query_params:
            queryset = queryset.filter(sender=user)
        elif 'recipient' in self.request.query_params:
            queryset = queryset.filter(recipient=user)
            
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        message.read_at = timezone.now()
        message.save()
        return Response({'status': 'message marked as read'})
        
        return queryset

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