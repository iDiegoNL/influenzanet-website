#!/bin/sh

export PERL5LIB=/home/flusurvey/perl/share/perl/5.12.4
perl /home/flusurvey/sql/send_email.pl
cat /home/flusurvey/sql/output.txt | /usr/sbin/sendmail -t -oi -oem
