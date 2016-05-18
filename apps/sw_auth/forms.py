from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from models import EpiworkUser
from django.utils.translation import ugettext_lazy as _
from apps.reminder.models import UserReminderInfo


attrs_dict = { 'class': 'required' }

password_dict = { 'class': 'required','placeholder':_("Enter your password") }

REMINDER_STATES = (
    (True, u'Recevoir la newsletter'),
    (False, u'Ne pas recevoir la newsletter'),
)

EMAIL_FIELD_SIZE = 255

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(label=_("Username"), max_length=255)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(
                _("Your Web browser doesn't appear to have cookies enabled. "
                  "Cookies are required for logging in."))

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    username = forms.RegexField(regex=r'(?u)^[\w.@+-_]+$',
                                max_length=255,
                                widget=forms.TextInput(attrs=dict(attrs_dict, placeholder=_("Username or email"))),
                                label=_("Username"), help_text=_("A Username or an email address with only letters, numbers or @ + - _ chars"),
                                error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=EMAIL_FIELD_SIZE, placeholder=_("Email address"))),
                             label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=password_dict, render_value=False),
                                label=_("Password"),
                                help_text=_("password, only letter, numbers and punctution"),
                                )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=password_dict, render_value=False),
                                label=_("Password (again)"))

    invitation_key = forms.CharField(
                        widget=forms.TextInput(attrs={'placeholder':_("Invitation key")}),
                        max_length=30,
                        label=_("Invitation key"),
                        help_text=_("Invitation key is not required to register"),
                        required=False)

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        try:
            user = EpiworkUser.objects.get(login__iexact=self.cleaned_data['username'])
        except EpiworkUser.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        user = EpiworkUser.objects.filter(email__iexact=self.cleaned_data['email'])
        if(len(user) == 0):
            return self.cleaned_data['email']
        raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))

    def clean(self):
        """
        Verify that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"), max_length=EMAIL_FIELD_SIZE)

    def clean_email(self):
        """
        Validates that an active user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]

        self.users_cache = EpiworkUser.objects.filter(email__iexact=email, is_active=True)
        if len(self.users_cache) == 0:
            # Check if any non active user exists with this email
            print email + " Doest exists"
            u = EpiworkUser.objects.filter(email__iexact=email, is_active=False)
            print(u)
            if len(u) > 0:
                raise forms.ValidationError(_("That e-mail address is associated with an inactive account. Did you activated ?"))
            raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        return email


class UserEmailForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"), max_length=EMAIL_FIELD_SIZE)

    def clean_email(self):
        """
        Validates that an active user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]
        try:
            self.users_cache = EpiworkUser.objects.filter(email__iexact=email)
        except EpiworkUser.DoesNotExist:
            raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        return email


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without
    entering the old password
    """
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput(attrs=password_dict))
    new_password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput(attrs=password_dict))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

class ReminderSettings(forms.Form):
    send_reminders = forms.BooleanField(label=_("Send reminders"),  widget=forms.RadioSelect(choices=REMINDER_STATES), required=False)

    def __init__(self, *args, **kwargs):

        self.instance = kwargs.pop('instance')

        self.reminder_info, _ = UserReminderInfo.objects.get_or_create(user=self.instance, defaults={'active': True, 'last_reminder': self.instance.date_joined})

        initial = kwargs.pop('initial', {})
        initial['send_reminders'] = self.reminder_info.active
        kwargs['initial'] = initial

        super(ReminderSettings, self).__init__(*args, **kwargs)

    def save(self):
        self.reminder_info.active = self.cleaned_data['send_reminders']
        self.reminder_info.save()


class EmailForm(forms.Form):
    email = forms.EmailField(label=_("Email"))

    def __init__(self, *args, **kwargs):

        self.epiwork_user = kwargs.pop('instance')

        initial = kwargs.pop('initial', {})
        initial['email'] = self.epiwork_user.email
        kwargs['initial'] = initial

        super(EmailForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        # check if email has been changed
        if email != self.epiwork_user.email:
            if EpiworkUser.objects.exclude(id=self.epiwork_user.id).filter(email=email).count():
                raise forms.ValidationError(_("This email is already in use"))
        return email
