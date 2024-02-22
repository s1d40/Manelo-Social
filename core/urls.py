"""
URL configuration for Manelo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include  # make sure include is imported
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# Import your views here
from .views import (
    HomeView, UserRegister, CustomLoginView, HomeRedirect, CustomLogoutView, MessageViewSet, chat_room
)

# Create a router and register your viewsets with it
router = DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', HomeRedirect, name='index'),
    path('signup/', UserRegister.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('user/<pk>/', HomeView.as_view(), name='home'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    # Include the router urls into your urlpatterns
    path('api/', include(router.urls)),  # This line includes all the routes defined by the router
    path('chatrooms/<int:chat_room_id>/', chat_room, name='chat_room'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
