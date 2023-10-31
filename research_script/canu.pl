#!/usr/bin/perl -w
use strict;
use warnings;
use FindBin qw($Bin);
use Getopt::Long;
use Cwd;
use File::Basename;

my $canu="/home/fanyucai/software/Canu/canu-1.5/Linux-amd64/bin/";
my $smrtanalysis="/home/Softwares/smrtanalysis_2.3.0/current/etc/setup.sh";
my $env="export LD_LIBRARY_PATH=/home/Softwares/gcc-5.2.0/lib64/:\$LD_LIBRARY_PATH";
my $gnuplot="/home/fanyucai/software/gnuplot/gnuplot-v5.0.6/bin";
my $mecat="/home/fanyucai/software/MECAT/Linux-amd64/bin";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";

my ($outdir,$subreads,$genomesize,$queue,$thread,$memory,$erro,$correct,$minlength);
$outdir||=getcwd;
$queue||="fat";
$thread||=30;
$memory||=200;
$erro||=0.01;
$correct||=40;
$minlength||=1000;
GetOptions(
    "r:s"=>\$subreads,
    "o:s"=>\$outdir,
    "z:s"=>\$genomesize,
    "q:s"=>\$queue,
    "t:s"=>\$thread,
    "m:s"=>\$memory,
    "e:s"=>\$erro,
    "l:s"=>\$minlength,
    "c:s"=>\$correct,
           );
sub usage{
    print qq{
This script will use canu to assembly genome.
usage:
perl $0 -r subreads.fastq -o $outdir -z 4700000 -q fat -c 40,60,80,100,1000
options:
-r          raw fastq subreads(force)
-z          genome size(froce)
-o          output directory(default:$outdir)
-q          which queue you run(default:fat)
-t          thread(default:30)
-m          memomry(default:300)
-l          Reads shorter than this are not loaded into the assembler(defualt:1000)
-c          correct the longest reads up to this coverage,choose one or several 40,50,60,80,100,1000(short plasmid)

Email:fanyucai1\@126.com
2017.8.1
    };
    exit;
}
sub qsub{
    my ($shell,$lines,$queue)=@_;
    $lines||=1;
    $queue||="big";
    my $cmd = "perl $qsub --lines $lines --queue $queue $shell";
    if(system ($cmd)!=0)
    {
        die "qsub [$shell] die with error : $cmd \n";
        exit;
    }
}
if(!$subreads||!$genomesize||!$correct)
{
    &usage();
}
my @depth=split(/\,/,$correct);
open(CA,">$outdir/canu.sh");
for (my $i=0;$i<=$#depth;$i++)
{
    system "mkdir -p $outdir/$depth[$i].x";
    system "ln -s $subreads $outdir/$depth[$i].x/subreads.fastq";
    if($depth[$i]<=40)
    {
        print CA "cd $outdir/$depth[$i].x && $env && export PATH=$canu:$gnuplot:\$PATH && canu -p canu -d $outdir/$depth[$i].x useGrid=0 gnuplotTested=false genomeSize=$genomesize maxMemory=$memory correctedErrorRate=0.01 -pacbio-raw subreads.fastq\n";
    }
    elsif($depth[$i]>40 && $depth[$i]<100)
    {
        print CA "cd $outdir/$depth[$i].x && $env && export PATH=$canu:$gnuplot:\$PATH && canu -p canu -d $outdir/$depth[$i].x corOutCoverage=$depth[$i] useGrid=0 gnuplotTested=false genomeSize=$genomesize maxMemory=$memory correctedErrorRate=0.01 -pacbio-raw subreads.fastq\n";
    }
    elsif($depth[$i]==100)
    {
        print CA "cd $outdir/$depth[$i].x && $env && export PATH=$canu:$gnuplot:\$PATH && canu -p canu -d $outdir/$depth[$i].x corOutCoverage=$depth[$i] useGrid=0 gnuplotTested=false genomeSize=$genomesize maxMemory=$memory correctedErrorRate=0.005 -pacbio-raw subreads.fastq\n";
    }
    elsif($depth[$i]==1000)
    {
        #for assembly short plasmid(http://canu.readthedocs.io/en/latest/faq.html#my-genome-is-at-or-gc-rich-do-i-need-to-adjust-parameters-what-about-highly-repetitive-genomes)
        print CA "cd $outdir/$depth[$i].x && $env && export PATH=$canu:$gnuplot:\$PATH && canu -p canu -d $outdir/$depth[$i].x corOutCoverage=1000 useGrid=0 gnuplotTested=false genomeSize=$genomesize maxMemory=$memory correctedErrorRate=0.01 -pacbio-raw subreads.fastq\n";
    }
    else
    {
        &usage();
    }
}
system "perl $qsub --queue $queue $outdir/canu.sh";

