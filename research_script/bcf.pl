#!/usr/bin/perl -w
use strict;
use warnings;
use Getopt::Long;
use Cwd;
use FindBin qw($Bin);
use File::Basename;
my $env="export LD_LIBRARY_PATH=/home/fanyucai/software/gcc/gcc-v6.1.0/lib64/:\$LD_LIBRARY_PATH && export PATH=/home/fanyucai/software/gcc/gcc-v6.1.0/bin/:\$PATH";
my $bfc="/home/fanyucai/software/bfc/bfc-master/bfc";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my $split="/home/fanyucai/software/SortMeRNA/sortmerna-2.1b/scripts/unmerge-paired-reads.sh";
my(@pe1,@pe2,$outdir,@prefix,@genomesize);
$outdir||=getcwd;

GetOptions(
    "a:s{1,}"=>\@pe1,       
    "b:s{1,}"=>\@pe2,      
    "o:s"=>\$outdir,      
    "p:s{1,}"=>\@prefix,
    "g:s{1,}"=>\@genomesize,
           );
sub usage{
    print qq{
This script will correcting sequencing errors from Illumina sequencing data.(using bcf)
usage:
perl -a sample1_1.fq sample2_1.fq -b sample1_2.fq sample2_2.fq -p sample1 sample2 -o outdir/ -g 4m 5m
options:
-a          pe1 reads(several split by space)
-b          pe2 reads(several split by space)
-p          prefix of output (several split by space)
-g          approx genome size (k/m/g allowed; change -k and -b) [unset]
-o          output directory

Yang J, Moeinzadeh M H, Kuhl H, et al. Haplotype-resolved sweet potato genome traces back its hexaploidization history[J]. Nature plants, 2017.

Email:fanyucai1\@126.com
2017.8.24
};
exit;
}
if(!@pe1||!@pe2||!@genomesize)
{
    &usage();
}
open(ERR,">$outdir/corrected_erro.sh");
for(my $k=0;$k<=$#genomesize;$k++)
{
    print ERR "$bfc -s $genomesize[$k] -t8 $pe1[$k] $pe2[$k]> $outdir/$prefix[$k].corrected.fq && ";
    print ERR "$split $outdir/$prefix[$k].corrected.fq $outdir/$prefix[$k]\_1.fq $outdir/$prefix[$k]\_2.fq\n";
}

system "$qsub $outdir/corrected_erro.sh";
