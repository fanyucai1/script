#!/usr/bin/perl -w
use strict;
use warnings;
use FindBin qw($Bin);
use Getopt::Long;
use Cwd;

my $file=shift;
my $seq=shift;
open(FA,"$seq");
my %hash;
my $name;
while(<FA>)
{
    chomp;
    if($_=~/\>/)
    {
        $name=substr($_,1);
    }
    else
    {
        $hash{$name}.=$_;
    }
}
open(IN,"$file");
open(OUT1,">micro.txt");
open(OUT2,">no_micro.txt");
my %hash1;
while(<IN>)
{
    chomp;
    my @array=split(/;/,$_);
    if($_=~/Bacteria/i || $_=~/Viruses/i || $_=~/Archaea/i)
    {
        $hash1{$array[0]}=1;
        print OUT1 $_,"\n";
    }
    else
    {
        print OUT2 $_,"\n";
    }
}
open(OUT3,">no_micro.fasta");
open(OUT4,">micro.fasta");
foreach my $key(keys %hash)
{
    if(!exists $hash1{$key})
    {
        print OUT3 ">$key","\n",$hash{$key},"\n";
    }
    else
    {
        print OUT4 ">$key","\n",$hash{$key},"\n";
    }
}