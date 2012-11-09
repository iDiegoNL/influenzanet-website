from django import forms
from django.conf import settings
from models import EpiworkUser
from django.utils.translation import ugettext_lazy as _
from apps.reminder.models import UserReminderInfo

attrs_dict = { 'class': 'required' }

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
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)"))
    
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
        try:
            user = EpiworkUser.objects.get(email__iexact=self.cleaned_data['email'])
        except EpiworkUser.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"), max_length=75)

    def clean_email(self):
        """
        Validates that an active user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]
       
        try:
            self.users_cache = EpiworkUser.objects.filter(email__iexact=email, is_active=True) 
        except EpiworkUser.DoesNotExist:
            raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        return email
            
class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without
    entering the old password
    """
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput)

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
    
class MySettingsForm(forms.Form):
    email = forms.EmailField(label=_("Email"))
    send_reminders = forms.BooleanField(label=_("Send reminders"), help_text=_("Check this box if you wish to receive weekly reminders throughout the flu season"), required=False)
    language = forms.ChoiceField(label=_("Language"), choices=settings.LANGUAGES)
    
    def __init__(self, *args, **kwargs):
                
        self.instance = kwargs.pop('instance')
        self.epiwork_user = kwargs.pop('epiwork')
        
        self.reminder_info, _ = UserReminderInfo.objects.get_or_create(user=self.instance, defaults={'active': True, 'last_reminder': self.instance.date_joined})

        initial = kwargs.pop('initial', {})
        initial['email'] = self.epiwork_user.email
        initial['send_reminders'] = self.reminder_info.active
        initial['language'] = self.reminder_info.language if self.reminder_info.language else settings.LANGUAGE_CODE
        kwargs['initial'] = initial

        super(MySettingsForm, self).__init__(*args, **kwargs)
        
        if len(settings.LANGUAGES) == 1:
            del self.fields['language']

    def clean_email(self):
        email = self.cleaned_data['email']
        # check if email has been changed
        if email != self.epiwork_user.email:
            if EpiworkUser.objects.exclude(id=self.epiwork_user.id).filter(email=email).count():
                raise forms.ValidationError(_("This email is already in use"))
        return email

    def save(self):
        if self.epiwork_user.email == self.epiwork_user.login:
            self.epiwork_user.username = self.cleaned_data['email']
        self.epiwork_user.email = self.cleaned_data['email']

        self.reminder_info.active = self.cleaned_data['send_reminders']
        
        if 'language' in self.cleaned_data:
            self.reminder_info.language = self.cleaned_data['language']

        #self.instance.save()
        self.reminder_info.save()
        self.epiwork_user.save()
