#!/usr/bin/perl

use MIME::Entity;
#use strict;
#use warnings;

do ("$ENV{HOME}/sql/addresses");

my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time);
my $filename=sprintf("/home/flusurvey/sql/incidence_%04d%02d%02d.csv", $year+1900, $mon+1, $mday);

system("psql -f /home/flusurvey/sql/incidence.sql ".
	   "--no-align --pset footer --field-separator ','".
	       " > $filename");

### Create the top-level, and set up the mail headers:
my $top = MIME::Entity->build(Type    =>"multipart/mixed",
			      From    => "$FROM",
			      To      => "$TO",
			      CC      => "$CC",
			      Subject => "Flusurvey weekly data $mday/".($mon+1)."/".($year+1900));

### Part #1: message
$top->attach(Data=>["Hi guys,\n\nThis your automated weekly email.\n\nCheers,\n  $name\n"], 
             Type=>"text/plain",
             Disposition=>"inline");

### Part #2: incidence data
$top->attach(Path=>"$filename",
             Type=>"text/csv",
             Disposition=>"attachment");

### Save it:
open MAIL, ">$ENV{HOME}/sql/output.txt" or die "open: $!";
$top->print(\*MAIL);
close MAIL;
