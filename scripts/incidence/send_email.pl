#!/usr/bin/perl

use MIME::Entity;
#use strict;
#use warnings;

do ("$ENV{HOME}/sql/addresses");

my $script_all="/home/flusurvey/sql/incidence_all.sql";
my $script_country="/home/flusurvey/sql/incidence_country.sql";

my $options="--no-align --pset footer --field-separator ','";

my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time);
my $filename_all=sprintf("/home/flusurvey/sql/incidence_all_%04d%02d%02d.csv", $year+1900, $mon+1, $mday);
my $filename_country=sprintf("/home/flusurvey/sql/incidence_country_%04d%02d%02d.csv", $year+1900, $mon+1, $mday);

system("psql -f $script_all $options > $filename_all");
system("psql -f $script_country $options > $filename_country");

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
$top->attach(Path=>"$filename_all",
             Type=>"text/csv",
             Disposition=>"attachment");
$top->attach(Path=>"$filename_country",
             Type=>"text/csv",
             Disposition=>"attachment");

### Save it:
open MAIL, ">$ENV{HOME}/sql/output.txt" or die "open: $!";
$top->print(\*MAIL);
close MAIL;
