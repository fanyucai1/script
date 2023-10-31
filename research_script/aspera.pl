#!/usr/bin/perl -w
use strict;
use warnings;
use Getopt::Long;
use Cwd;
use FindBin qw($Bin);

my ($outdir,$sra,$type);
my $aspera="/home/fanyucai/.aspera/connect";
$outdir||=getcwd;
GetOptions(
    "type:s"=>\$type,
    "o:s"=>\$outdir,
    "sra:s"=>\$sra,   
           );

sub usage{
    print qq{
This script will download file from NCBI or EMBL using Aspera.
usage:
perl $0 -sra "/blast/db/16SMicrobial.tar.gz" -type ncbi -o $outdir
            or
perl $0 -sra  "/vol1/fastq/SRR346/SRR346368/SRR346368.fastq.gz " -type embl -o $outdir
            or
perl $0 -sra SRR5319286 -type ncbi -o $outdir

Email:fanyucai1\@126.com
2017.12.27
version 1.0
2018.4.8
version 2.0 fix SRR
    };
    exit;
}
if(! $sra ||!$type)
{
    &usage();
}
my $string;
if($type=~/ncbi/i)
{
    if($sra=~/SRR/)
    {
        $sra=~s/^\s+//;
        $sra=~s/\s+$//;
        my $ID=substr($sra,0,6);
        $string="anonftp\@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/SRR/$ID/$sra/$sra.sra";
    }
    else
    {
        $string="anonftp\@ftp.ncbi.nlm.nih.gov:";
        $string.=$sra;
    }
}
elsif($type=~/embl/i)
{
    $string="era-fasp\@fasp.sra.ebi.ac.uk:";
    $string.=$sra;
}
else
{
    &usage();
}

system "echo '$aspera/bin/ascp -T -k1 -i $aspera/etc/asperaweb_id_dsa.openssh $string $outdir'>$outdir/aspera.sh";

`nohup sh $outdir/aspera.sh&`;
