#!/usr/bin/perl -w
use strict;
use warnings;
use Getopt::Long;
use FindBin qw($Bin);
use Cwd;
use File::Basename;

my ($ref,$denovo,$outdir);
$outdir||=getcwd;
my $mummer="/home/fanyucai/software/mummer/MUMmer3.23/";
GetOptions(
    "r:s"=>\$ref,       
    "d:s"=>\$denovo,       
    "o:s"=>\$outdir,
           );

sub usage{
    print qq{
This script will alignment reference and denovo genome use mummer.
usage:
perl $0 -ref reference.fna -d denovo.fna -o $outdir

options:
-r          refernce genome fasta
-d          denovo genome fasta
-o          output directory(default:$outdir)

Paper:
HISEA: HIerarchical SEed Aligner for PacBio data
Improved de novo Genome Assembly: Linked-Read Sequencing Combined with Optical Mapping Produce a High Quality Mammalian Genome at Relatively Low Cost


Email:fanyucai1\@126.com
2018.3.9
    };
    exit;
}

######################################################################
open(MUM,">$outdir/mummer.sh");

print MUM "$mummer/nucmer --maxmatch -c 1000 -d 10 -banded -D 5 -l 100 $ref $denovo\n";