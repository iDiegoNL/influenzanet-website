from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.conf import settings
from django.contrib.auth.models import User

from registration.forms import RegistrationForm
from apps.reminder.models import UserReminderInfo

attrs_dict = {'class': 'required'}

class UnicodeRegistrationForm(RegistrationForm):
    username = forms.RegexField(regex=r'(?u)^[\w.@+-]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    
class UnicodeUserChangeForm(UserChangeForm):
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'(?u)^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})

class UnicodeUserCreationForm(UserCreationForm):
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'(?u)^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})


class EmailSettingsForm(forms.Form):
    email = forms.EmailField(label=_("Email"))
    send_reminders = forms.BooleanField(label=_("Send reminders"), help_text=_("Check this box if you wish to receive weekly reminders throughout the flu season"), required=False)
    language = forms.ChoiceField(label=_("Language"), choices=settings.LANGUAGES)
    
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        self.reminder_info, _ = UserReminderInfo.objects.get_or_create(user=self.instance, defaults={'active': True, 'last_reminder': self.instance.date_joined})

        initial = kwargs.pop('initial', {})
        initial['email'] = self.instance.email
        initial['send_reminders'] = self.reminder_info.active
        initial['language'] = self.reminder_info.language if self.reminder_info.language else settings.LANGUAGE_CODE
        kwargs['initial'] = initial

        super(EmailSettingsForm, self).__init__(*args, **kwargs)
        
        if len(settings.LANGUAGES) == 1:
            del self.fields['language']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(id=self.instance.id).filter(email=email).count():
            raise forms.ValidationError(_("This email is already in use"))
        return email

    def save(self):
        if self.instance.email == self.instance.username:
            self.instance.username = self.cleaned_data['email']
        self.instance.email = self.cleaned_data['email']

        self.reminder_info.active = self.cleaned_data['send_reminders']
        
        if 'language' in self.cleaned_data:
            self.reminder_info.language = self.cleaned_data['language']

        self.instance.save()
        self.reminder_info.save()


class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', )
     
    def clean_username(self):
        value = self.cleaned_data['username']

        if User.objects.exclude(pk=self.instance.pk).filter(username=value).count():
            raise forms.ValidationError(_("A user with this username already exists"))

        return value

