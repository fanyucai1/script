#!/usr/bin/perl -w
use strict;
use warnings;
use FindBin qw($Bin);
use Getopt::Long;
use Cwd;
use File::Basename;

my $cDNA_Cupcake="/home/fanyucai/software/cDNA_Cupcake/cDNA_Cupcake/";
my $python="/home/fanyucai/software/python/Python-v2.7.9/bin/python";
my($outdir,$clstr,$fasta,$hq,$csv);
$outdir||=getcwd;

GetOptions(
    "clstr:s"=>\$clstr,       
     "fa:s"=>\$fasta,
     "o:s"=>\$outdir,
     "hq:s"=>\$hq,
     "csv:s"=>\$csv,
           );
sub usage{
    print qq{
This script will Run subsampling to draw rarefaction curves.
usage:
perl $0 -clstr unigene.fa.clstr -fa cluster.fa -hq  -o $outdir

options:
-hq         HQ isoform sequences,this file is usually called hq_isoforms.fasta.
-clstr      from cdhit output
-fa         fasta file from cd-hit output
-o          output directory(default:$outdir)
-csv        all.cluster_report.csv

Email:fanyucai1\@126.com
2018.3.6
    };
    exit;
}

system "mkdir -p $outdir/test";
open(IN1,$csv);
my (%CCS,$fl_reads,$nfl_reads,$total_reads);

while(<IN1>)
{
    chomp;
    if($_!~/cluster_id,read_id,read_type/)
    {
        my @array=split(/\,/,$_);
        if($array[2]=="FL")
        {
            $fl_reads++;
        }
        if($array[2]=="NonFL")
        {
            $nfl_reads++;
        }
        my @array1=split(/\|/,$array[0]);
        $CCS{$array1[1]}{$array[2]}++;
        $total_reads++;
    }
}

open(IN,$clstr);
open(OUT1,">$outdir/count.txt");
my(%unigene,$seqname);
while(<IN>)
{
    chomp;
    if($_=~/^\>/)
    {
        my @array=split;
        $seqname="PB.";
        $seqname.=$array[1];
        $seqname.=".1";
    }
    else
    {
        my @array=split(/\//,$_);
        my $index1=index($array[1],"f");
        my $index2=index($array[1],"p");
        $unigene{$seqname}{"FL"}+=substr($array[1],$index1+1,$index2-$index1-1);
        $unigene{$seqname}{"NonFL"}+=substr($array[1],$index2);
    }
}