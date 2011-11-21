import MySQLdb

from django.core.management.base import NoArgsCommand, BaseCommand 
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from apps.reminder.models import UserReminderInfo
from apps.survey.models import SurveyUser

class Command(NoArgsCommand):

    @transaction.commit_on_success
    def handle_noargs(self, **options):
        c = MySQLdb.connect(host="localhost", user="root", passwd="", db="ggm_existing_tmp", charset='utf8')
        cursor = c.cursor ()
        cursor.execute ("SELECT * FROM `meter` WHERE laatste_mail >= 117 AND wil_herinnering =  '1'")

        rows = cursor.fetchall()
        for i, row in enumerate(rows):
            meter_id, UUID, email, naam, postcode, geb_datum, geslacht, password, _pw_new, laatste_meting, laatste_mail, herinnering, reken_postcode, wil_herinnering, stress = row
            print i, email,

            u = authenticate(username=email[:30], password=password)
            if not u:
                print "SKIPPING"
                continue

            u.set_password(_pw_new)
            u.save()
            print

        cursor.close ()
        c.close ()

