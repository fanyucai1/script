#!/usr/bin/perl -w
use strict;
use warnings;
use Getopt::Long;
use Cwd;
use Cwd 'abs_path';
use Config::IniFiles;
use FindBin qw($Bin);
use File::Basename;

my $bwa="/local_data1/software/bwa/bwa-0.7.17/bwa";
my $bowtie="/local_data1/software//bowtie/bowtie-1.2.2-linux-x86_64";
my $bowtie2="/local_data1/software//bowtie2/bowtie2-2.3.4.1-linux-x86_64";
my $samtools="/local_data1/software/samtools/samtools-1.9/samtools";
my $picard="/local_data1/software//picard/picard.jar";
my $blast="/local_data1/software//blast+/ncbi-blast-2.7.1+/bin/makeblastdb";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my $hisat2="/local_data1/software//hisat2/hisat2-2.1.0";
my $star="/local_data1/software/STAR/STAR-2.6.0a/bin/Linux_x86_64/STAR";
my($ref,$prefix,$outdir,$gtf);
$outdir||=getcwd;
$prefix||="ref";
GetOptions(
    "r:s"=>\$ref,
    "p:s"=>\$prefix,
    "o:s"=>\$outdir,
    "g:s"=>\$gtf,
           );
if (!$ref)
{
    &usage();
}
sub usage{
    print qq{
This script will index reference using blast+,bwa,bowtie,bowtie2,samtools,STAR and picard.
usage:
perl $0 -r /path/to/directory/ref.fna -g /path/to/diectory/##.gtf -o $outdir -p prefix

options:
-r          your reference fna(force)
-p          prefix of output(default:ref)
-o          output directory(default:$outdir)
-g          gtf (or gff)file

Email:fanyucai1\@126.com
Vesion:2.0
2018.8.6
    };
    exit;
}
system "mkdir -p $outdir";
$ref=abs_path($ref);
$outdir=abs_path($outdir);
system "ln -s $ref $outdir/$prefix.fasta";
open(INDEX,">$outdir/index.sh");
#bwa index
print INDEX "cd $outdir && $bwa index -a bwtsw $prefix.fasta\n";
#picard index
print INDEX "cd $outdir && java -jar -Xmx20g $picard CreateSequenceDictionary REFERENCE=$prefix.fasta OUTPUT=$prefix.dict\n";
#bowtie index
print INDEX "cd $outdir && $bowtie/bowtie-build $prefix.fasta $prefix.fasta\n";
#bowtie2 index
print INDEX "cd $outdir && $bowtie2/bowtie2-build $prefix.fasta $prefix.fasta\n";
#samtools index
print INDEX "cd $outdir && $samtools faidx $prefix.fasta\n";
#makeblastdb
print INDEX "cd $outdir && $blast -in $prefix.fasta -dbtype nucl\n";
#make hisat2 index
print INDEX "cd $outdir && $hisat2/hisat2-build -p 10 $prefix.fasta $prefix.fasta\n";
#make STAR index
if(-e $gtf)
{
    $gtf=abs_path($gtf);
    system "mkdir -p $outdir/genomeDir";
    print INDEX "cd $outdir && $star --runThreadN 20 --runMode genomeGenerate --genomeDir $outdir/genomeDir --genomeFastaFiles $prefix.fasta --sjdbGTFfile $gtf\n";
}
`cd $outdir && perl $qsub $outdir/index.sh`;
