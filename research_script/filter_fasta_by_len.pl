#!/usr/bin/perl
use strict;
use warnings;

if($#ARGV ne 1)
{
 print "perl $0 test.fa 1000 >out.fasta\n";
exit;
}
my $fasta=shift;
my $minlen = shift;
open(FA,"$fasta");
my $name;
my %hash;
while(<FA>)
{
	chomp;
	if($_=~/^\>/)
	{
		$name=$_;
	}
	else
	{
		$hash{$name}.=$_;
	}
}

foreach my $key(keys %hash)
{
	if(length($hash{$key})>=$minlen)
	{
		print $key,"\n",$hash{$key},"\n";
	}
}
