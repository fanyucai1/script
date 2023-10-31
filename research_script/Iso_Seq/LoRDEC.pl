#!/usr/bin/perl -w
use strict;
use warnings;
use Cwd;
use File::Basename;
use Getopt::Long;
use FindBin qw($Bin);

my $glibc="export LD_LIBRARY_PATH=/home/fanyucai/software/glibc/glibc-v2.14/lib:\$LD_LIBRARY_PATH";
my $LoRDEC="/home/fanyucai/software/LoRDEC/lordec-bin_0.7_linux64/";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my $normalize="/home/fanyucai/software/trinity/trinityrnaseq-Trinity-v2.5.1/util/insilico_read_normalization.pl";
my $fq2fa="/home/fanyucai/software/idba/idba-master/bin/fq2fa";

my ($left,$right,$outdir,$type,$pacbio,$line);
$outdir||=getcwd;
$type||="RF";
GetOptions(
    "l:s"=>\$left,
    "r:s"=>\$right,
    "o:s"=>\$outdir,
    "t:s"=>\$type,
    "p:s"=>\$pacbio,
           );
sub usage{
    print qq{
This script will normalize NGS data and then correct the pacbio data.
usage:
perl $0 -l sample1.1.fq,sample2.1.fq -r sample1.2.fq,sample2.2.fq -o $outdir

options:
-l              left reads(several split by comma)
-r              right reads(several split by comma)
-o              output directory(default:$outdir)
-t              Strand-specific RNA-Seq read orientation: RF(default) or FR
-p              pacbio long read FASTA/Q file

Email:fanyucai1\@126.com
2018.3.6
    };
    exit;
}
if(!$left||!$right||$type)
{
    &usage();
}
######################################A survey of the complex transcriptome from the highly polyploid sugarcane genome using full-length isoform sequencing and de novo assembly from short read sequencing
open(NO,">$outdir/normal.sh");
print NO "perl $normalize --seqType fq --JM 50G --max_cov 50 --left $left --right $right --pairs_together --output $outdir/normalize/ --CPU 10 --PARALLEL_STATS\n";
print NO "$fq2fa --merge $outdir/normalize/left.norm.fq $outdir/normalize/right.norm.fq $outdir/NGS.fa\n";
$line=`wc -l $outdir/normal.sh`;
chomp($line);
`perl $qsub --ppn 5 --lines $line $outdir/normal.sh`;

######################################http://www.atgc-montpellier.fr/lordec/
open(CO,">$outdir/correct.sh");
print CO "$glibc && $LoRDEC/lordec-correct -i $pacbio -2 $outdir/NGS.fa -T 10 -s 2 -k 21 -o $outdir/LoRDEC_corrected.fasta\n";
`perl $qsub --ppn 5 $outdir/correct.sh`;