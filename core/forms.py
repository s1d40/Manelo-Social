from django import forms
from .models import ManeloUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = ManeloUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'profile_picture')
        


class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput, label=_('Remember me'))

    def __init__(self, request=None, *args, **kwargs):
        """
        Initialize the form with an optional request argument.
        """
        super(CustomAuthenticationForm, self).__init__(request=request, *args, **kwargs)

    def confirm_login_allowed(self, user):
        """
        Override this method to add extra checks for the user,
        for example, you might want to disallow login for non-active users.
        """
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive."),
                code='inactive',
            )
        # Additional custom validations can be added here

    class Meta:
        model = ManeloUser
        fields = ('username', 'password', 'remember_me')
