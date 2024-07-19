import logging
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import UnitedUserProfile
from .validators import (
    validate_customer_phone_number,
    validate_customer_city, validate_customer_zip_code)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column

logger = logging.getLogger(__name__)


class UnitedSignUpForm(UserCreationForm):
    """
    Form for user signup with personal
    info and address, extending UserCreationForm.
    """
    first_name = forms.CharField(
        max_length=30, required=True, widget=forms.TextInput(attrs={
            'placeholder': _('First name')}), help_text='Required.'
    )
    last_name = forms.CharField(
        max_length=30, required=True, widget=forms.TextInput(attrs={
            'placeholder': _('Last name')}), help_text='Required.'
    )
    email = forms.EmailField(
        max_length=254, widget=forms.EmailInput(attrs={'placeholder': _(
            'Email')}), help_text='Required. Enter a valid email address.'
    )
    phone_number = forms.CharField(
        max_length=15, required=True, validators=[
            validate_customer_phone_number],
        widget=forms.TextInput(attrs={'placeholder': _(
            'Phone number')}),
    )
    city = forms.CharField(
        max_length=50, required=True, validators=[validate_customer_city],
        widget=forms.TextInput(attrs={'placeholder': _('City')})
    )
    zip_code = forms.CharField(
        max_length=10, required=True, validators=[validate_customer_zip_code],
        widget=forms.TextInput(attrs={'placeholder': _('Zip code')})
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password', 'placeholder': _('Password')}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password', 'placeholder': _(
                'Password confirmation')}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        """
        Configures UnitedSignUpForm to use the
        User model and define form fields.
        """
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'password1', 'password2',
            'phone_number', 'city', 'zip_code'
        )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and configure form helper settings.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

    def save(self, commit=True):
        """
        Save the user instance and create associated
        profile.
        """
        user = super().save(commit=False)

        if not user.username:
            user.username = self.cleaned_data['email']

        if commit:
            user.save()
            UnitedUserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                city=self.cleaned_data['city'],
                zip_code=self.cleaned_data['zip_code']
            )

            logger.debug("User and profile saved successfully")

            return user


class UnitedSignInForm(forms.Form):
    """
    Form for requesting a sign in from user.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': _('Email')}),
        label=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Password')}),
        label=False
    )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
        label=_('Remember Me')
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize the UnitedSignInForm with
        custom form helper settings and layout.
        """
        super(UnitedSignInForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('email', placeholder=_('Email'), css_class='mb-2'),
            Field('password', placeholder=_('Password'), css_class='mb-2'),
            'remember_me',
        )


class ContactForm(forms.Form):
    """
    A form for users to submit contact information and a message.
    """
    name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={'placeholder': _('Enter your name')}),
        label='',
        help_text=''
    )
    phone_number = forms.CharField(
        max_length=15, required=True, validators=[
            validate_customer_phone_number],
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter your phone number')}),
        label='',
        help_text=''
    )
    email = forms.EmailField(
        max_length=254, required=True,
        widget=forms.EmailInput(attrs={'placeholder': _('Enter your email')}),
        label='',
        help_text=''
    )
    message = forms.CharField(
        max_length=350, required=True,
        widget=forms.Textarea(attrs={
            'placeholder': _('Your message here... Up to 350 characters')}),
        label='',
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize the ContactForm with custom form helper settings.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
