from django.core.management.base import NoArgsCommand
from django.db import connection, transaction
from ...models import EpiworkUser
from apps.sw_auth.models import EpiworkUserManager

class Command(NoArgsCommand):
    help = 'Shuffle the auth table (by rebuilding it: caution)'
  
    def handle_noargs(self, **options):
        cursor = connection.cursor()
        table = 'sw_auth_epiworkuser'
        table_new = table + '_new'
        cursor.execute("CREATE TABLE %s AS SELECT * FROM %s ORDER BY id" % (table_new,table,))
        cursor.execute("DROP TABLE %s" % table)
        cursor.execute("ALTER TABLE %s RENAME TO %s" % (table_new, table,))
        transaction.commit_unless_managed()