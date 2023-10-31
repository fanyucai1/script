#!usr/bin/perl -w
use warnings;
use strict;
use Getopt::Long;

  
my $edirect="/home/fanyucai/software/edirect/";
if($#ARGV ne 1)
{
     print "usage:perl $0 seq.list out.fasta\n";
     exit;
}
my $list=shift;
my $out=shift;
open(LI,"$list");
my $n=0;
while(<LI>)
{
     chomp;
     $n++;
     if($n==1)
     {
          system  "$edirect/esearch -db nucleotide -query \"$_\" | $edirect/efetch -format fasta > $out";
     }
     else
     {
          system  "$edirect/esearch -db nucleotide -query \"$_\" | $edirect/efetch -format fasta >> $out";
     }
}