from optparse import make_option
from django.core.management.base import CommandError, BaseCommand
from django.contrib.sites.models import Site

from django.db import connection, transaction

class Command(BaseCommand):
    help = 'Cleanup tokens'
    args = 'create|load'
    option_list = BaseCommand.option_list + (
        make_option('-t', '--table', action='store', type="string",
                dest='table',help='Data table to use', default=None),
        make_option('-o', '--output', action='store_true', dest='output',help='Output', default=False),
    )

    def handle(self, *args, **options):
        
        command = args[0]
    
        if command == 'create':
            self.create_table(self)
            return
        if options['table'] is None:
            table = 'pollster_results_intake'
        else:
            table = options['table']
            
        query = """ select "user", string_agg(zip,',') as zip, string_agg(code_reg,',') as reg, string_agg(code_dep,',') as dep from (
    select "user", "global_id", last_value("Q3") OVER (PARTITION BY global_id ORDER BY timestamp) as zip  from """ + table + """ 
) a left join geo_levels g on a.zip=g.code_com group by "user" """

        cursor = connection.cursor()
        
        cursor.execute(query)
        
        data = cursor.fetchall()
        
        cursor.close()
        
        def as_code(code, max_length):
                if not code:
                    return 'NULL'
                code = list(set(code.split(',')))
                # As only one value
                if len(code) == 1:
                    code = str(code[0])
                    if len(code) > max_length:
                        print  " [%s] over %d chars" % (code, max_length,)
                        return 'NULL'
                    if not code.isalnum():
                        print " [%s] is not alnum" % code
                        return 'NULL'
                    return "'%s'" % code
                return 'NULL'
            
        rows = []
        for d in data:
            user = d[0]
            zip = d[1]
            reg = d[2]
            dep = d[3]
            zip = as_code(zip, 5) 
            dep = as_code(dep, 3)
            reg = as_code(reg, 2)
            q = "(%s,%s,%s,%s)" % (str(user), zip, reg, dep, )
            rows.append(q)
        self.update_table(rows, output=options['output'])
        
    @transaction.commit_on_success
    def update_table(self, rows, output):    
        print 'Truncate table'
        cursor = connection.cursor()
        cursor.execute("truncate table swauth_location")
        cursor.close()
        print 'Insert data'
        query = "insert into swauth_location (user_id,zip_code_key,code_reg,code_dep) values "
        query = query + ','.join(rows)
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        if output:
            print 'output query to location.sql'
            out = open('location.sql','w')
            out.write(query +';')
            out.close()
            
    @transaction.commit_on_success
    def create_table(self):
        query = """
        CREATE TABLE swauth_location
        (
          user_id integer NOT NULL,
          zip_code_key character varying(5),
          code_reg character(2),
          code_dep character(3),
          CONSTRAINT pk_swauth_location PRIMARY KEY (user_id ),
          CONSTRAINT fk_location_user FOREIGN KEY (user_id)
              REFERENCES auth_user (id) MATCH SIMPLE
              ON UPDATE NO ACTION ON DELETE CASCADE
        )"""
        cursor = connection.cursor()
        cursor.execute(query)      
        
    

