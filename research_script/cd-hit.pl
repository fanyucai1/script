#!/usr/bin/perl -w
use strict;
use warnings;
use FindBin qw($Bin);
use Getopt::Long;
use File::Basename;
use Cwd;

my $cdhit="/home/fanyucai/software/cdhit/cdhit-master";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my ($outdir,$identity,$fasta,$kind,$thread,$queue);
$outdir||=getcwd;
$identity||=0.95;
$thread||=10;
$queue||="fat";

GetOptions(
    "i:s"=>\$identity,       
    "o:s"=>\$outdir,
    "fa:s"=>\$fasta,
    "k:s"=>\$kind,       
    "m:s"=>\$memory,
    "t:s"=>\$thread,
           );
sub usage{
    print qq{
This script will use cd-hit for clustering and comparing large sets of protein or nucleotide sequences.
usage:
perl $0  -i 0.95 -o outdir -fa protein.fa -k prot -t 8
options:
-i          sequence identity threshold, default 0.95
-fa         fasta sequence
-k          nucl or prot
-t          number of threads, default 10
-o          output directory,default $outdir
-q          which queue you will run

Pootakham W, Sonthirod C, Naktang C, et al. De novo hybrid assembly of the rubber tree genome reveals evidence of paleotetraploidy in Hevea species[J]. Scientific Reports, 2017, 7.
Email:fanyucai1\@126.com
2017.8.30
    };
    exit;
}
system "mkdir -p $outdir/cdhit";
if(!$fasta||!$kind)
{
    &usage();
}
my $program;
if($kind=~/nucl/i)
{
    $program="$cdhit/cd-hit-est";
}
if($kind=~/prot/i)
{
    $program="$cdhit/cd-hit";
}
system "echo ' $program -i $fasta -c $identity -M 0 -T $thread -o $outdir/cdhit'>$outdir/cdhit.sh";
`perl $qsub --queue $queue --ppn $thread $outdir/cdhit.sh`;
