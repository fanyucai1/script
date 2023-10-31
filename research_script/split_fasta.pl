#!/usr/bin/perl -w
use strict;
use warnings;
use Cwd;
use FindBin qw($Bin);
use Getopt::Long;
use Bio::SeqIO;
use File::Basename;
my ($fasta,$num,$outdir);
GetOptions(
    "fa:s"=>\$fasta,
    "n:s"=>\$num,
    "o:s"=>\$outdir,
        );
sub usage{
    print qq{
This script will split fasta files.
usage:
perl $0 -fa seq.fasta -o out_directory -n 600
options:
-fa                 input fasta
-n                  the counts of sequence per fasta file
-o		    output_directory
Email:fanyucai1\@126.com
2016.12.2
    };
    exit;
}
if(!$fasta||!$num||!$outdir)
{
    &usage();
}
system "mkdir -p $outdir/";
my $base=basename($fasta);
my $in  = Bio::SeqIO->new(-file  =>"$fasta");
my $count = 0;
my $fcount = 1;
my $out = Bio::SeqIO->new(-file => ">$outdir/$base.$fcount.split.fa", -format=>'Fasta');
while (my $seq = $in->next_seq())
{
        $count++;
        if ($count % $num==0)
        {
                $fcount++;
                $out =Bio::SeqIO->new(-file => ">$outdir/$base.$fcount.split.fa", -format=>'Fasta');
        }
        $out->write_seq($seq);
}
