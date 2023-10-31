#!/usr/bin/perl -w
use strict;
use warnings;
use FindBin qw($Bin);
use Getopt::Long;
use Cwd;

my $kraken="/home/fanyucai/software/kraken/kraken-v1.0";
my $db="/home/fanyucai/software/kraken/minikraken_20171019_8GB/";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my $env="export LD_LIBRARY_PATH=/home/Softwares/gcc-5.2.0/lib64/:\$LD_LIBRARY_PATH";

my ($fasta,$outdir,$keywords);
$outdir||=getcwd;
$keywords||="1";

GetOptions(
    "fa:s"=>\$fasta,
    "o:s"=>\$outdir,
    "k:s"=>\$keywords,
           );
sub usage{
    print qq{
This script will classified sequences using kraken(http://ccb.jhu.edu/software/kraken/MANUAL.html).
usage:
perl $0 -fa input.fasta -o /path/to/directory
options:
-fa         the sequence of input
-o          outputdirectory(default:$outdir)
-k          the keywords you want grep

Email:fanyucai1\@126.com
2017.6.19
    };
    exit;
}
sub qsub()
{
	my ($shfile, $queue, $ass_maxproc) = @_ ;
    $queue||="all";
    $ass_maxproc||=5;
    my $cmd = "perl $qsub --maxproc $ass_maxproc --queue $queue --reqsub $shfile --independent" ;
    my $flag=system($cmd);
    if($flag !=0)
    {
		die "qsub [$shfile] die with error : $cmd \n";
        exit;
	}
}
if(!$fasta)
{
    &usage();
}
system "mkdir -p $outdir";
open(TAX1,">$outdir/kraken1.sh");
print TAX1 "$env && $kraken/kraken --db $db $fasta > $outdir/sequences.kraken\n";
&qsub("$outdir/kraken1.sh");

open(TAX2,">$outdir/kraken2.sh");
print TAX2 "$env && $kraken/kraken-translate --db $db $outdir/sequences.kraken > $outdir/sequences.labels";
&qsub("$outdir/kraken2.sh");

if($keywords!~"1")
{
    system "grep $keywords $outdir/sequences.labels >$outdir/keywords.txt";
}




