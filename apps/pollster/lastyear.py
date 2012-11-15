from django.db import connection

def get_previous_year_data(user_id, global_id, shortname):
 cursor = connection.cursor()
 query = "select * from pollster_%s_lastyear where \"global_id\"='%s' and \"user\"='%s'" % (shortname, global_id, str(user_id))
 cursor.execute(query)
 desc = cursor.description
 res = cursor.fetchone()
 return dict(zip([col[0] for col in desc], res))