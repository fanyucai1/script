#!/usr/bin/perl -w
use strict;
use warnings;
use FindBin qw($Bin);
use Cwd;
use Getopt::Long;

my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my $gce="/home/fanyucai/software/gce/gce-1.0.0/";
my $R="/home/fanyucai/software/R/R-v3.2.0/bin/Rscript";
my($pe1,$pe2,$outdir,$length,$queue);
$length||=150;
$queue||="fat";
$outdir||=getcwd;
GetOptions(
    "a:s"=>\$pe1,
    "b:s"=>\$pe2,
    "o:s"=>\$outdir,
    "l:s"=>\$length,
    "q:s"=>\$queue,
           );
sub usage{
    print qq{
This script will use gce(ftp://ftp.genomics.org.cn/pub/gce) to eastimate genome size.
usage:
perl $0 -a pe1.fq -b pe2.fq -o /path/to/directory/
options:
-a      5' reads
-b      3'reads
-o      output directory
-l      maximum read length(default:150)
-q      which queue will run(default:fat)
        
Email:fanyucai1\@126.com
2017.5.23
    };
    exit;
}
if(!$pe1||!$pe2||!$outdir||!$queue)
{
    &usage();
}

system "mkdir -p $outdir/";
`echo $pe1 >$outdir/list.txt`;
`echo $pe2 >>$outdir/list.txt`;

open(RUN1,">$outdir/gce.sh");
print RUN1 "cd $outdir/ && $gce/kmerfreq/kmer_freq_hash/kmer_freq_hash -i 600000000 -k 17 -t 8 -o 0 -L $length -l list.txt";
print RUN1 " && $gce/gce -f output.freq.stat  >gce.table 2>gce.log\n";
`nohup perl $qsub --queue $queue $outdir/gce.sh &`;
