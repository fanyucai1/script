#!/usr/bin/perl -w
use strict;
use warnings;
use Cwd;
use FindBin qw($Bin);
use Getopt::Long;
use File::Basename;

my $subreads=shift;
my $contigs=shift;
my $outdir||=getcwd;
my $mummer=" /home/fanyucai/software/mummer/mummer-4.0.0/bin/";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my $python="/home/fanyucai/software/python/Python-v2.7.9/bin/python";
my $sc="/home/fanyucai/software/FinisherSC/finishingTool-master/finisherSC.py";

if(!$subreads||!$contigs)
{
    print "usage:\nperl $0 subreads.fastq contig.fa $mummer\n";
    print "fanyucai1\@126.com\n";
    exit;
}
system "mkdir -p $outdir/finish";
open(SU,"$subreads");
open(NE,">$outdir/finish/raw_reads.fasta");
my $i=0;
while(<SU>)
{
    chomp;
    $i++;
    if($_=~/\>/)
    {
 
            print NE ">Seg$i\n";
    }
    else
    {
        print NE "$_\n";
    }
}
close SU;
close NE;
open(SU,"$contigs");
open(NE,">$outdir/finish/contigs.fasta");
$i=0;
while(<SU>)
{
    chomp;
    $i++;
    if($_=~/\>/)
    {
 
        print NE ">Seg$i\n";
    }
    else
    {
        print NE "$_\n";
    }
}
system "echo '$python $sc -par 20 $outdir/finish/ /home/fanyucai/software/mummer/mummer-4.0.0/bin/'>$outdir/finish/run.sh";

`perl $qsub --queue fat $outdir/finish/run.sh`;