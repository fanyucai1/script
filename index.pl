#!/usr/bin/perl -w
use strict;
use warnings;
use Getopt::Long;
use Cwd;
use Cwd 'abs_path';
use FindBin qw($Bin);
use File::Basename;

my $bwa="/software/bwa/0.7.17/bwa-0.7.17/bwa";
my $bowtie="/software/bowtie/bowtie-1.2.2-linux-x86_64";
my $bowtie2="/software/bowtie2/2.3.4.3/bowtie2-2.3.4.3-linux-x86_64";
my $samtools="/software/samtools/1.9/samtools-1.9/bin/samtools";
my $picard="/software/picard/2.8.12/picard.jar";
my $blast="/software/blast/ncbi-blast-2.8.1+/bin/makeblastdb";
my $qsub="/data/fanyucai/qsub_sge.pl";
my $hisat2="/software/hisat2/hisat2-2.1.0";
my $star="/software/STAR/STAR-2.7.0e/bin/Linux_x86_64/STAR";
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
if(defined $gtf)
{
    $gtf=abs_path($gtf);
    system "mkdir -p $outdir/genomeDir";
    print INDEX "cd $outdir && $star --runThreadN 20 --runMode genomeGenerate --genomeDir $outdir/genomeDir --genomeFastaFiles $prefix.fasta --sjdbGTFfile $gtf\n";
}
`cd $outdir && perl $qsub $outdir/index.sh`;
