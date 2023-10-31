#!/usr/bin/perl -w
use strict;
use warnings;
use Cwd;
use FindBin qw($Bin);
use Getopt::Long;

my($blast_out,$outdir,$len);
$outdir||=getcwd;
GetOptions(
    "b:s"=>\$blast_out,       
    "o:s"=>\$outdir,       
    "len:s"=>\$len,       
           );

sub usage{
    print qq{
This script will parse the blast out.
usage:
perl $0 -b blast.out -o $outdir -len $len
options:
-b      the blast out(from blast+ and outformat is 6)
-o      output directory

Email:fanyucai1\@126.com
2017.12.25
    };
    exit;
}
open(IN,$blast_out);
my %hash;
while(<IN>)
{
    chomp;
    my @array=split;
    $hash{$array[0]}{$array[1]}+=$array[3];
}
print "#query\tref\tmapping_length\n";
foreach my $key1 (keys %hash)
{
    foreach my $key2(keys %{$hash{$key1}})
    {
        if($hash{$key1}{$key2}>=$len)
        {
            print $key1,"\t",$key2,"\t",$hash{$key1}{$key2},"\n";
        }
    }
}