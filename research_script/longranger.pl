#!/usr/bin/perl -w
use strict;
use warnings;
use Cwd;
use FindBin qw($Bin);
use Getopt::Long;
use File::Basename;

my $longranger="/home/fanyucai/software/Long_Ranger/longranger-2.1.3/longranger";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";

sub usage{
    print qq{
This script will mapping the 10X genome short reads to references.
usage:
perl $0 -ref reference.fa -o outputdirectory -fastqs /path/to/fastq/driectory/ --sample A,B,C --id
options:
-id             A unique run id, used to name output folder
-sample         Prefix of the filenames of FASTQs to select.For example, if your FASTQs are named:subject1_S1_L001_R1_001.fastq.gz then set --sample=subject1
-fastqs         Path of folder created by 10x demultiplexing or bcl2fastq.


Email:fanyucai1\@126.com
2017.5.19
    };
    exit;
}
my ($ref,$outdir,$fastqs,$sample,$id);
GetOptions(
   "ref:s"=>\$ref,
   "o:s"=>\$outdir,
   "fastqs:s"=>\$fastqs,
   "sample:s"=>\$sample,
   "id:s"=>\$id,
           );

if(!$ref || !$outdir||!$fastqs)
{
    &usage();
}
system "mkdir -p $outdir/";
#first index reference
open(INDEX,">$outdir/index.sh");
print INDEX "cd $outdir && $longranger mkref $ref";
#`perl $qsub $outdir/index.sh`;
#system "rm $outdir/index.sh";

my $base=basename $ref;
my $dir=dirname $ref;
my @array=split(/\./,$base);
#mapping
open(MAP,">$outdir/mapping.sh");
print MAP "cd $outdir && $longranger align --reference=$dir/refdata-$array[0]/ --fastqs=$fastqs --sample=$sample --id=$id";

`perl $qsub $outdir/mapping.sh`;