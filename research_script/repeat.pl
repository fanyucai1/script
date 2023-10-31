#!/usr/bin/perl -w
use strict;
use warnings;
use FindBin qw($Bin);
use Getopt::Long;
use Cwd;
use File::Basename;

my $repeatmasker="/home/fanyucai/software/RepeatMasker/RepeatMasker/";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my $out2gff="/home/fanyucai/software/RepeatMasker/RepeatMasker/rmOutToGFF3.pl";
#############http://bedops.readthedocs.io/en/latest/content/reference/file-management/conversion/rmsk2bed.html
my $rmsk2bed="/home/fanyucai/software/BEDOPS/bin/rmsk2bed";
my $env="export PATH=/home/fanyucai/software/BEDOPS/bin/:\$PATH";
my $trf="/home/fanyucai/software/RepeatMasker/TRF/trf";
my $trf2gff="/home/fanyucai/script/TRF2GFF.py";#https://github.com/Adamtaranto/TRF2GFF
my $python="/home/fanyucai/software/python/Python-v2.7.9/bin/python";
my($genome,$outdir,$species,$engine,$cpu,$ppn);
$outdir||=getcwd;
$engine||="wublast";
$cpu||=30;
$species||="All";
GetOptions(
    "genome:s"=>\$genome,       
    "species:s"=>\$species,
    "engine:s"=>\$engine,
    "cpu:s"=>\$cpu,
    "o:s"=>\$outdir,    
           );
sub usage{
    print qq{
This script will run repeatmasker(Version: 4.0.7).
usage:
perl $0 -genome assembly_genome.fa -species human -engine wublast -cpu 30 -o $outdir

options:
-genome     scaffold or contig sequence(fasta)
-engine     Use an alternate search engine:wublast(default)|ncbi
-cpu        The number of processors to use in parallel(default:30)
-o          output directory(default:$outdir)
-species    default:(All)
            Other commonly used species:
            human,mouse,rattus,"ciona savignyi",mammal, carnivore, rodentia, rat, cow, pig, cat, dog, chicken, fugu,
            danio, "ciona intestinalis" drosophila, anopheles, elegans,diatoaea, artiodactyl, arabidopsis, rice, wheat, and maize

Email:fanyucai1\@126.com
2017.12.27
    };
    exit;
}
if(!$genome)
{
    &usage();
}
system "mkdir -p $outdir";
system "mkdir -p $outdir/trf";
open(OUT,">$outdir/repeatmasker.csv");
print OUT "Query\tstart\tend\tRepeat_name\tSmith-Waterman score\tStrand\t";
print OUT "Percentage,substitutions\tPercentage, deleted bases\tPercentage,inserted bases\tBases in query, past match\tRepeat class\t";
print OUT "Bases in complement of the repeat consensus sequence\tMatch start\tMatch end\tUnique ID\tHigher-scoring match (optional)\n";

open(RUN,">$outdir/repeat.sh");
print RUN "cd $outdir && $repeatmasker/RepeatMasker -norna -no_is -species $species -parallel $cpu -e $engine -s -gff -dir $outdir $genome && ";
my $filename=basename $genome;
print RUN "cd $outdir && $env && $rmsk2bed < $filename.out >>$outdir/repeatmasker.csv\n";
##############################run RepeatProteinMask
print RUN "cd $outdir && $repeatmasker/RepeatProteinMask -noLowSimple -engine wublast -pvalue 0.0001 $genome\n";
#############################run trf
print RUN "cd $outdir/trf && $trf $genome 2 7 7 80 10 50 2000 -d -h && $python $trf2gff -d $filename.2.7.7.80.10.50.2000.dat -o trf.gff3\n";
system "cd $outdir && perl $qsub --ppn 15 $outdir/repeat.sh";

