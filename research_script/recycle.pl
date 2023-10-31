#!/usr/bin/perl -w
use strict;
use warnings;
use Cwd;
use FindBin qw($Bin);
use Getopt::Long;
use File::Basename;

my $python="/home/fanyucai/software/python/Python-v2.7.9/bin/python";
my $recycle="/home/fanyucai/software/python/Python-v2.7.9/bin/recycle.py";
my $fa2fg="/home/fanyucai/software/python/Python-v2.7.9/bin/make_fasta_from_fastg.py";
my $bwa="/home/fanyucai/software/bwa/bwa-0.7.12/bwa";
my $samtools="/smrtlinks/smrtlink/smrtcmds/bin/samtools";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";

my($fg,$pe1,$pe2,$kmer);
GetOptions(
   "fg:s"=>\$fg,
   "pe1:s"=>\$pe1,
   "pe2:s"=>\$pe2,
   "k:s"=>\$kmer,   
);
sub usage{
    print qq{
Recycler is a tool designed for extracting circular sequences from de novo assembly graphs. It can be applied on isolate as well as metagenome and plasmidome data. 
usage:
perl $0 -pe1 pe1.fq -pe2 pe2.fq -fq xxx.fastg -k 77
options:
-pe1        5 reads
-pe2        3 reads
-fq         assembly graph FASTG file to process,for spades 3.6+, assembly_graph.fastg
-k          maximum k-mer length used by the assembler

Email:fanyucai1\@126.com
2017.6.22
    };
    exit;
}
if(!$fg||!$pe1||!$pe2||!$kmer)
{
    &usage();
}
my $outdir=dirname $fg;
my $base=basename $fg;
if($fg=~".fastg")
{
    $base=substr($base,0,length($base)-6);
}
else
{
    &usage();
}

open(BAM,">$outdir/mapping.sh");
print BAM "$python $fa2fg -g $fg\n";
print BAM "cd $outdir && $bwa index $base.nodes.fasta\n";
print BAM "cd $outdir && $bwa mem $base.nodes.fasta $pe1 $pe2 | $samtools view -buS - > reads_pe.bam\n";
print BAM "cd $outdir && $samtools view -bF 0x0800 reads_pe.bam > reads_pe_primary.bam\n";
print BAM "cd $outdir && $samtools sort reads_pe_primary.bam -o reads_pe_primary.sort\n";
print BAM "cd $outdir && $samtools index reads_pe_primary.sort.bam\n";
print BAM "cd $outdir && $python $recycle -g $fg -k $kmer -b reads_pe_primary.sort.bam -i True\n";

my $line=`wc -l $outdir/mapping.sh`;
chomp($line);
`perl $qsub --lines $line $outdir/mapping.sh`;