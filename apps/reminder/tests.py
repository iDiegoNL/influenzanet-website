import unittest
from datetime import datetime, timedelta, date

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings
from django import forms

from mock import Mock, patch, patch_object

from apps.survey.models import SurveyUser

from .send import create_message, send
from .models import NO_INTERVAL, WEEKLY_WITH_BATCHES, UserReminderInfo, ReminderSettings, NewsLetter, NewsLetterTemplate, get_upcoming_dates, get_prev_reminder_date, get_prev_reminder, get_reminders_for_users, ReminderError, ReminderError
from .forms import NewsLetterForm

class ReminderTestCase(unittest.TestCase):
    def setUp(self):
        ReminderSettings.objects.all().delete()
        NewsLetter.objects.all().delete()
        NewsLetterTemplate.objects.all().delete()
        User.objects.all().delete()

        self.old_languages = settings.LANGUAGES
        settings.LANGUAGES = (('en', 'English'), ('de', 'German'), ('fr', 'French'))

    def tearDown(self):
        settings.LANGUAGES = self.old_languages

    def test_get_upcoming_updates(self):
        def test(first_date, last_date, result):
            result = list(result) 
            self.assertEqual(first_date, result[0][0])
            self.assertEqual(last_date, result[-1][0])

        site = Site.objects.get()

        self.assertEquals([], list(get_upcoming_dates(datetime(2010, 10, 1, 15, 0, 0))))

        settings = ReminderSettings.objects.create(
            site=site,
            send_reminders=False,
            begin_date=datetime(2010, 9, 1, 14, 0, 0),
            interval=14,
        )

        self.assertEquals([], list(get_upcoming_dates(datetime(2010, 10, 1, 15, 0, 0))))

        settings.send_reminders = True
        settings.save()

        test(datetime(2010, 9, 15, 14, 0), datetime(2010, 12, 8, 14, 0), get_upcoming_dates(datetime(2010, 10, 1, 15, 0, 0)))
         
    def test_get_prev_reminder_date(self):
        site = Site.objects.get()

        self.assertEquals(None, get_prev_reminder_date(datetime(2010, 12, 12)))

        settings = ReminderSettings.objects.create(
            site=site,
            send_reminders=False,
            begin_date=datetime(2010, 9, 1, 14, 0, 0),
            interval=7,
        )

        self.assertEquals(None, get_prev_reminder_date(datetime(2010, 12, 12)))

        settings.send_reminders = True
        settings.save()

        self.assertEquals(None, get_prev_reminder_date(datetime(2010, 9, 1, 13, 0, 0)))
        self.assertEquals(datetime(2010, 9, 1, 14, 0, 0), get_prev_reminder_date(datetime(2010, 9, 1, 14, 0, 0)))
        self.assertEquals(datetime(2010, 9, 1, 14, 0, 0), get_prev_reminder_date(datetime(2010, 9, 8, 13, 0, 0)))
        self.assertEquals(datetime(2010, 9, 8, 14, 0, 0), get_prev_reminder_date(datetime(2010, 9, 8, 15, 0, 0)))

    def test_get_prev_reminder_with_newsletter(self):
        september_first = datetime(2010, 9, 1, 14, 0, 0)

        site = Site.objects.get()
        settings = ReminderSettings.objects.create(
            site=site,
            send_reminders=True,
            begin_date=september_first,
            interval=7,
        )

        newsletter = NewsLetter.objects.create(date=september_first, sender_email="test@example.org", sender_name="Test")
        newsletter.translate('en')
        newsletter.subject = "English subject"
        newsletter.message = "English message"
        newsletter.save()

        newsletter.translate('de')
        newsletter.subject = "German subject"
        newsletter.message = "German message"
        newsletter.save()

        result = get_prev_reminder(september_first)

        self.assertEqual("test@example.org", result['en'].sender_email)
        self.assertEqual("English subject", result['en'].subject)
        self.assertEqual("German subject", result['de'].subject)
        self.assertFalse('fr' in result)

    def test_get_prev_reminder_with_template(self):
        september_first = datetime(2010, 9, 1, 14, 0, 0)

        site = Site.objects.get()
        settings = ReminderSettings.objects.create(
            site=site,
            send_reminders=True,
            begin_date=september_first,
            interval=7,
        )

        template = NewsLetterTemplate.objects.create(is_default_reminder=True, sender_email="test@example.org", sender_name="Test")
        template.translate('en')
        template.subject = "English subject"
        template.message = "English message"
        template.save()

        template.translate('de')
        template.subject = "German subject"
        template.message = "German message"
        template.save()

        result = get_prev_reminder(september_first)

        self.assertEqual("test@example.org", result['en'].sender_email)
        self.assertEqual("English subject", result['en'].subject)
        self.assertEqual("German subject", result['de'].subject)
        self.assertFalse('fr' in result)

    def test_get_prev_reminder_irregular_intervals(self):
        september_first  = datetime(2010, 9, 1, 14, 0, 0)
        september_second = datetime(2010, 9, 2, 14, 0, 0)

        site = Site.objects.get()
        settings = ReminderSettings.objects.create(
            site=site,
            send_reminders=True,
            begin_date=september_first,
            interval=NO_INTERVAL,
        )

        # no newsletter: nothing to send
        self.assertEquals(None, get_prev_reminder_date(datetime(2010, 12, 12)))

        # default reminder template is not used
        template = NewsLetterTemplate.objects.create(is_default_reminder=True, sender_email="test@example.org", sender_name="Test")
        template.translate('en')
        template.subject = "Template subject"
        template.message = "Template message"
        template.save()
        self.assertEquals(None, get_prev_reminder_date(datetime(2010, 12, 12)))

        # but newsletters are used
        newsletter = NewsLetter.objects.create(date=september_first, sender_email="test@example.org", sender_name="Test")
        newsletter.translate('en')
        newsletter.subject = "September first"
        newsletter.message = "September first"
        newsletter.save()
        result = get_prev_reminder(datetime(2010, 9, 1, 20))
        self.assertEqual("test@example.org", result['en'].sender_email)

        # newer newsletters have preference
        newsletter = NewsLetter.objects.create(date=september_second, sender_email="test@example.org", sender_name="Test")
        newsletter.translate('en')
        newsletter.subject = "September second"
        newsletter.message = "September second"
        newsletter.save()
        result = get_prev_reminder(datetime(2010, 9, 2, 20))
        self.assertEqual("test@example.org", result['en'].sender_email)

        # even for irregular reminders the begin-date is respected
        self.assertEqual(None, get_prev_reminder(datetime(2008, 9, 2, 20)))

    def test_get_reminders_for_users(self):
        september_first = datetime(2010, 9, 1, 14, 0, 0)

        site = Site.objects.get()
        settings = ReminderSettings.objects.create(
            site=site,
            send_reminders=True,
            begin_date=september_first,
            interval=7,
        )

        newsletter = NewsLetter.objects.create(date=september_first, sender_email="test@example.org", sender_name="Test")
        newsletter.translate('en')
        newsletter.subject = "English subject"
        newsletter.save()

        newsletter.translate('de')
        newsletter.subject = "German subject"
        newsletter.save()

        for i, (language, active, last_reminder, expected) in enumerate([
            ('en', False, None, None),              # inactive: don't send
            (None, True, None, "English subject"),  # no language set: use default language
            ('en', True, None, "English subject"),  # english: use english
            ('de', True, None, "German subject"),   # german: use german
            ('fr', True, None, "English subject"),   # french not available: use default language
            ('en', True, september_first, None),    # already sent, don't send again
        ]):

            user = User.objects.create(username="user%s" % i)
            info = UserReminderInfo.objects.create(user=user, last_reminder=last_reminder, active=active, language=language)

            result = list(get_reminders_for_users(september_first, User.objects.filter(id=user.id)))
            if expected is None:
                self.assertEqual([], result)
            else:
                self.assertEqual(1, len(result))
                self.assertEqual(expected, result[0][1].subject, "%s, %s, %s, '%s' failed with actual: '%s'" %(language, active, last_reminder, expected, result[0][1].subject))

    def test_create_message(self):
        class Message(object):
            def __init__(self):
                self.message = 'this is text'
                
        user = User.objects.create(username="user")

        text_base, html = create_message(user, Message(), 'nl')
        self.assertTrue('this is text' in text_base)
        self.assertTrue('<body' in html)
        self.assertTrue('this is text' in html)
        self.assertFalse('<body' in text_base)

        self.assertFalse('You have received this email because' in html)
        self.assertTrue('U ontvangt deze mail omdat' in html, html)

    def test_irregular_intervals_form(self):
        form = NewsLetterForm() 
        self.assertEquals(forms.ChoiceField, type(form.fields['date']))

        settings = ReminderSettings.objects.create(
            site=Site.objects.get(),
            send_reminders=True,
            begin_date=datetime(2010, 9, 1, 14, 0, 0),
            interval=NO_INTERVAL,
        )

        form = NewsLetterForm() 
        self.assertEquals(forms.DateField, type(form.fields['date']))

    def test_email_errors(self):
        return
        # not implemented right now; I can't find the proper way to make email sending fail for test-purposes

        user = User.objects.create(username="malformed-user", email="")
        info = UserReminderInfo.objects.create(user=user)
         
        september_first = datetime(2010, 9, 1, 14, 0, 0)

        site = Site.objects.get()
        settings = ReminderSettings.objects.create(
            site=site,
            send_reminders=True,
            begin_date=september_first,
            interval=7,
        )

        newsletter = NewsLetter.objects.create(date=september_first, sender_email="test@example.org", sender_name="Test")
        newsletter.translate('en')
        newsletter.subject = "English subject"
        newsletter.message = "English message"
        newsletter.save()

        send(datetime(2010, 10, 10, 12, 0, 0), user, newsletter, 'en')


    def test_week_after_action(self):
        september_first = datetime(2010, 9, 1, 14, 0, 0)

        site = Site.objects.get()
        settings = ReminderSettings.objects.create(
            site=site,
            send_reminders=True,
            begin_date=september_first,
            interval=WEEKLY_WITH_BATCHES,
        )

        for days_after_startday in [0, 7]:
            newsletter = NewsLetter.objects.create(date=september_first + timedelta(days=days_after_startday), sender_email="test@example.org", sender_name="Test")
            newsletter.translate('en')
            newsletter.subject = "English subject - %s" % days_after_startday
            newsletter.message = "English message"
            newsletter.save()

        for weekday in range(7):
            user = User.objects.create(username="week-after-user-%s" % weekday)
            info, _ = UserReminderInfo.objects.get_or_create(user=user, defaults={'active': True, 'language': 'en'})
            info.last_reminder = september_first - timedelta(days=8) # last reminder: long enough ago, is tested elsewhere
            info.save()

            survey_user, _ = SurveyUser.objects.get_or_create(user=user, deleted=False)
            survey_user.last_participation_date=september_first - timedelta(days=7 - weekday)
            survey_user.save()

        for days_after_startday in range(8):
            result = list(get_reminders_for_users(september_first + timedelta(days=days_after_startday, minutes=1), User.objects.filter(username__startswith="week-after-user-")))
            self.assertEqual(days_after_startday + 1 if days_after_startday < 7 else 7, len(result), "Fail for day %s, len: %s" % (days_after_startday, len(result)))
            if len(result) >= 1:
                user, reminder, language = result[0]
                self.assertTrue(str(0 if days_after_startday < 7 else 7) in reminder.subject, reminder.subject)

        NewsLetter.objects.filter(date__gt=september_first).delete()
        result = list(get_reminders_for_users(september_first + timedelta(days=0, minutes=1), User.objects.filter(username__startswith="week-after-user-")))
        self.assertEqual(1, len(result))
        result = list(get_reminders_for_users(september_first + timedelta(days=7, minutes=1), User.objects.filter(username__startswith="week-after-user-")))
        self.assertEqual(0, len(result))

        NewsLetter.objects.all().delete()
        result = list(get_reminders_for_users(september_first + timedelta(minutes=1), User.objects.filter(username__startswith="week-after-user-")))
        self.assertEqual(0, len(result))

