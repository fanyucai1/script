#!/usr/bin/perl -w
use strict;
use warnings;
use FindBin qw($Bin);
use Getopt::Long;
use Cwd;
use Cwd 'abs_path';
my $Rscript="/local_data1/software/R/R-v3.4.0/bin/Rscript";
my $miRBase="/local_data1/reference/miRBase/mature.fa";
my $psRobot="/local_data1/software/psRobot/psRobot_v1.2/";
my $miRanda="/local_data1/software/miRanda/miRanda-3.3a/bin/miranda";
my $TargetFinder="/local_data1/software/TargetFinder/TargetFinder-master/";
my $FASTA35="/local_data1/software/FASTA/fasta-35.4.12/bin";
my $perl="/local_data1/software/perl/perl-v5.28.0/bin/perl";
my $RNAhybrid="/local_data1/software/RNAhybrid/RNAhybrid-v2.1.2/bin/";

my($outdir,$mRNA,$species,$database);
GetOptions(
    "m:s"=>\$mRNA,
    "o:s"=>\$outdir,
    "sp:s"=>\$species,
    "db:s"=>\$database,
           );
sub usage{
    print qq{
This script will find potential small RNA targets on a large scale using psRobot.

options:
-m      mRNA fasta sequence
-o      output directory
-sp     plant(pl) or animal(an):force
     
Email:fanyucai1\@126.com
2018.9
    };
    exit;
}
$outdir||=getcwd;
$mRNA=abs_path($mRNA);
$database||=$miRBase;
open(SH,">$outdir/shell.sh");
if($species=~/pl/)
{
    print SH "$psRobot/psRobot_tar -s $database -t $mRNA -o $outdir/psRobot.txt\n";
    print SH "export PATH=$FASTA35:\$PATH && perl $TargetFinder/targetfinder.pl -s $database -d $mRNA";
}
elsif($species=~/an/)
{
    print SH "$miRanda $mRNA $miRBase -out $outdir/miRanda.txt\n";
    print SH "$RNAhybrid/RNAhybrid ";
}
else
{
    system "You must choose your species\n\n";
    exit;
}
