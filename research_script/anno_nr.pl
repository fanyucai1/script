#!/usr/bin/perl -w
use strict;
use warnings;
use FindBin qw($Bin);
use Getopt::Long;
use Cwd;
use Cwd 'abs_path';

my($query,$nr,$outdir,$diamond,$map,$fa_split,$hmmer,$blastplus,$go,$qsub);
$diamond="/local_data1/software/diamond/diamond";
$nr="/local_data1/reference/diamond_nr/diamod_nr.dmnd";
$fa_split="/local_data1/software/fasta-splitter/fasta-splitter.pl";
$qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
$map="/local_data1/reference/Gene_Ontology/accession2go";#ftp://ftp.pir.georgetown.edu/databases/idmapping/(awk -F"\t" '{if($8~"GO") print $4"\t"$8}' idmapping.tb >accession2go)
$go="/local_data1/reference/Gene_Ontology/go-basic.obo";#http://geneontology.org/page/download-ontology
$outdir||=getcwd;

GetOptions(
    "q:s"=>\$query,
    "o:s"=>\$outdir,
           );
sub usage{
    print qq{
This script will annotate the nr and GO database.
usage:
perl $0 -q query.fa -o $outdir
options:
-q          query fasta sequence
-o          output directory

Email:fanyucai1\@126.com
2018.9
    };
    exit;
}
if(!$query)
{
    &usage();
}
$query=abs_path($query);
$outdir=abs_path($outdir);
system "perl $fa_split --n-parts 10  --out-dir $outdir $query";
my @array=glob("$outdir/*part*");
open(SH,">$outdir/mapping.sh");
foreach my $key(@array)
{
    print SH "$diamond blastx -q $key -e 0.00001 -p 30 -d $nr -o $key.m8 -f 6 -k 1 -l 20 --top 1 --more-sensitive\n";
}
if(! -e "$outdir/blast.out")
{
    system "perl $qsub $outdir/mapping.sh";
    system "cat $outdir/*m8 >$outdir/blast.out";
    system "rm $outdir/*part*";
}
my($total,$nr_num,$go_num);
$total=`grep -c \\> $query`;
chomp($total);
#################################################parse blast.out
open(BL,"$outdir/blast.out");
my %hash1;
while(<BL>)
{
    chomp;
    if($_!~/#/)
    {
        $nr_num++;
        my @array=split(/\t/,$_);
        $hash1{$array[0]}=$array[1];#query2accession
    }
}
#############################################parse nr2go
open(MP,"$map");
my %hash2;
while(<MP>)
{
    chomp;
    if($_!~/#/)
    {
        my @array=split(/\t/,$_);
        $hash2{$array[0]}=$array[1];#accession2go
    }
}
############################################parse go classify
open(GO,"$go");
my $ID;
my %hash3;
while(<GO>)
{
    chomp;
    if($_=~/^id: (\S+)/)
    {
        $ID=$1;
    }
    if($_=~/^namespace: (\S+)/)
    {
        $hash3{$ID}=$1;
    }
   
}
##########################################
open(OUT1,">$outdir/nr_anno_details.txt");
open(OUT2,">$outdir/nr_anno_stat.txt");
open(OUT3,">$outdir/nr_anno_bar.txt");
print OUT1 "#query\ttarget\tGO_ID\n";
my %hash4;
my %hash5;
foreach my $key(keys %hash1)
{
    if(exists $hash2{$hash1{$key}})
    {
        $go_num++;
        print OUT1 "$key\t$hash1{$key}\t$hash2{$hash1{$key}}\n";
        my @array=split(/\;/,$hash2{$hash1{$key}});
        for(my $i=0;$i<=$#array;$i++)
        {
            $array[$i]=~s/\s//;
            $hash5{$array[$i]}++;
            $hash4{$hash3{$array[$i]}}++;  
        }
    }
    else
    {
        print OUT1 "$key\t$hash1{$key}\n";
    }
}
print OUT2 "Total\t$total\n";
print OUT2 "Nr_num\t$nr_num\n";
print OUT2  "GO\t$go_num\n";
foreach my $key(keys %hash4)
{
    print OUT2 $key,"\t",$hash4{$key},"\n";
}
print OUT3 "GO_ID\tCounts\tType\n";
foreach my $key(keys %hash5)
{
    print OUT3 "$key\t$hash5{$key}\t$hash3{$key}\n";
}

