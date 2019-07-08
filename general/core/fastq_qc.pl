#!/usr/bin/perl -w
use strict;
use warnings;
use Getopt::Long;
use Cwd;
use Cwd 'abs_path';
use FindBin qw($Bin);
my (@pe1,@pe2,@prefix);
my $trim="/software/Trimmomatic/Trimmomatic-0.39/trimmomatic-0.39.jar";
my $java="/software/java/jdk1.8.0_202/bin/java";
my $qsub="/home/fanyucai/bin/qsub_sge.pl";
my $len||=75;
my $read||=150;
my $adapter||="TruSeq3-PE";
my $seq;
my $outdir||=getcwd;
if($adapter eq "TruSeq3-PE")
{
    $seq="/software/Trimmomatic/Trimmomatic-0.39/adapters/TruSeq3-PE.fa";
}

if($adapter eq "TruSeq2-PE")
{
    $seq="/software/Trimmomatic/Trimmomatic-0.39/adapters/TruSeq2-PE.fa";
}
GetOptions(
    "pe1:s{1,}"=>\@pe1,
    "pe2:s{1,}"=>\@pe2,
    "p:s{1,}"=>\@prefix,
    "o:s"=>\$outdir,
    "minL:s"=>\$len,
    "a:s"=>\$adapter,
    "r:s"=>\$read,
);
sub usage{
    print qq{
This script will quality control fastq file.
usage:
perl $0 -pe1 sample1.1.fq(.gz) sample2.1.fq(.gz) -pe2 sample1.2.fq(.gz) sample2.2.fq(.gz) -p sample1 sample2 -minL 150 -a TruSeq3-PE -q cu -o $outdir 
Options:
-pe1            5' reads several split by space(froce)
-pe2            3'reads several split by space (froce)
-o              output directory(default:$outdir)
-p              the prefix of output several split by space(force)
-minL           min length of quality control(default:75)
-r              read length(default:150)
-a              PE:TruSeq2-PE (as used in GAII machines) and TruSeq3-PE (as used by HiSeq and MiSeq machines)

Email:fanyucai1\@126.com
2018.8.16
   };
    exit;
}
if(!@pe1 || !@pe2||!@prefix)
{
    &usage();
}
system "mkdir -p $outdir/";

open(QC,">$outdir/clean.sh");
for(my $i=0;$i<=$#pe1;$i++)
{
    $pe1[$i]=abs_path($pe1[$i]);
    $pe2[$i]=abs_path($pe2[$i]);
    if($pe1[0]=~/gz$/)
    {
        print QC "java -jar -Xmx40g $trim PE -threads 10 $pe1[$i] $pe2[$i] $outdir/$prefix[$i]\_1.clean.fq.gz $outdir/$prefix[$i]\_1_un.fq.gz $outdir/$prefix[$i]\_2.clean.fq.gz $outdir/$prefix[$i]\_2_un.fq.gz CROP:$read ILLUMINACLIP:$seq:2:30:10:true LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:$len && ";
    }
    else
    {
        print QC "java -jar -Xmx40g $trim PE -threads 10 $pe1[$i] $pe2[$i] $outdir/$prefix[$i]\_1.clean.fq $outdir/$prefix[$i]\_1_un.fq.gz $outdir/$prefix[$i]\_2.clean.fq $outdir/$prefix[$i]\_2_un.fq.gz CROP:$read ILLUMINACLIP:$seq:2:30:10:true LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:$len && ";
    }
    print QC "rm $outdir/$prefix[$i]\_1_un.fq.gz $outdir/$prefix[$i]\_2_un.fq.gz\n";
}
system "perl $qsub $outdir/clean.sh";
