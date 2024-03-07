#!/usr/bin/perl -w
use strict;
use warnings;
use Getopt::Long;
use Config::IniFiles;
use File::Basename;
use Cwd;
use FindBin qw($Bin);
my $outdir||=getcwd;
my(@pe1,@pe2,@insert,$max_rd_len,@kmer);
$max_rd_len||=150;
my $soapdenovo="/home/fanyucai/software/Soapdenovo2/SOAPdenovo2-r240";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my $SSPACE="/home/fanyucai/software/SSPACE/SSPACE-STANDARD-3.0_linux-x86_64/SSPACE_Standard_v3.0.pl";
my $GapCloser="/home/fanyucai/software/GapCloser/GapCloser";
my $python="/home/fanyucai/software/python/Python-v2.7.9/bin/python";
my $quast="/home/fanyucai/software/quast/quast-4.5/quast.py";
my $queue||="fat";
my $cpu||=20;
my $kdepth||=2;
GetOptions(
    "pe1:s{1,}"=>\@pe1,
    "pe2:s{1,}"=>\@pe2,
    "insert:s{1,}"=>\@insert,
    "o:s"=>\$outdir,
    "r:s"=>\$max_rd_len,
    "k:s{1,}"=>\@kmer,
    "q:s"=>\$queue,
    "cpu:s"=>\$cpu,
);
sub usage {
    print qq {
This script will use soapdenovo to assembly microbiome genome.
usage:
perl $0 -pe1 sample1_1.fq sample2_1.fq -pe2 sample1_2.fq sample2_2.fq -insert 500 2000 -r 150 -k 17 19 21 23 63 67 77 -o $outdir -q fat -cpu 20
optionts:
 -pe1	        5 reads(several split by space)
 -pe2           5 reads(several split by space)      
 -insert        insert size(several split by space)
 -o             output directory(default:$outdir)
 -r             max read length(defualt:150)
 -k             the kmer(several split by space)
 -q             which queue you will run(default:fat)
 -cpu           cpu number(default:20)

Email:fanyucai1\@126.com
version2.0
2017.11.6
};
 exit; 
}
if(!@pe1 ||!@pe2||!@insert)
{
    &usage();
}
#####################make diretory
system "mkdir -p $outdir";
################assembly soapdenovo
        my $soap_contig;
        open(FH1,">$outdir/soapdenovo_1.sh");
        open(FH2,">$outdir/gapcloser_2.sh");
        system "mkdir -p $outdir/soapdenovo/";
        #first get the soapdenovo config
        system "echo max_rd_len=$max_rd_len>$outdir/soapdenovo/soap.config";
        for (my $k=0;$k<=$#insert;$k++)
        {
            my $number=$k+1;
            if ($insert[$k]<=2000)
            {
                system "echo [LIB]>>$outdir/soapdenovo/soap.config";
                system "echo avg_ins=$insert[$k] >>$outdir/soapdenovo/soap.config";
                system "echo reverse_seq=0 >>$outdir/soapdenovo/soap.config";
                system "echo asm_flags=3 >>$outdir/soapdenovo/soap.config";
                system "echo rank=1 >>$outdir/soapdenovo/soap.config";
                system "echo pair_num_cutoff=3 >>$outdir/soapdenovo/soap.config";
                system "echo map_len=32 >>$outdir/soapdenovo/soap.config";
                system "echo q1=$pe1[$k] >>$outdir/soapdenovo/soap.config";
                system "echo q2=$pe2[$k] >>$outdir/soapdenovo/soap.config";
            }
           else
            {
                system "echo [LIB]>>$outdir/soapdenovo/soap.config";
                system "echo avg_ins=$insert[$k] >>$outdir/soapdenovo/soap.config";
                system "echo reverse_seq=1 >>$outdir/soapdenovo/soap.config";
                system "echo asm_flags=2 >>$outdir/soapdenovo/soap.config";
                system "echo rank=2 >>$outdir/soapdenovo/soap.config";
                system "echo pair_num_cutoff=3 >>$outdir/soapdenovo/soap.config";
                system "echo map_len=32 >>$outdir/soapdenovo/soap.config";
                system "echo q1=$pe1[$k] >>$outdir/soapdenovo/soap.config";
                system "echo q2=$pe2[$k]>>$outdir/soapdenovo/soap.config";
            }
        }
        #run soapdenovo
        system "mkdir -p $outdir/sspace/";
        open(LB,">$outdir/sspace/Library.txt");
        for (my $i=0;$i<=$#insert;$i++)
        {
            my $j=$i+1;
            if($insert[$i]<=800)
            {
                print LB "LB$j bwa $pe1[$i] $pe2[$i] $insert[$i] 0.25 FR\n";
            }
            else
            {
                print LB "LB$j bwa $pe1[$i] $pe2[$i] $insert[$i] 0.5 FR\n";
            }
        }
        for (my $t=0;$t<=$#kmer;$t++)
        {
            system "mkdir -p $outdir/soapdenovo/kmer.$kmer[$t]/" ;
            if ($kmer[$t]<=63)
            {
                print FH1 "$soapdenovo/SOAPdenovo-63mer all -s $outdir/soapdenovo/soap.config -K $kmer[$t] -o $outdir/soapdenovo/kmer.$kmer[$t]/out -p $cpu -F -R -E -w -u -d $kdepth\n";
            }
            else
            {
                print FH1 "$soapdenovo/SOAPdenovo-127mer all -s $outdir/soapdenovo/soap.config -K $kmer[$t] -o $outdir/soapdenovo/kmer.$kmer[$t]/out -p $cpu -F -R -E -w -u -d $kdepth\n";
            }
            #do gapcloser and sspace
            if ($max_rd_len<155)
            {
                
                print FH2 "$GapCloser -b $outdir/soapdenovo/soap.config -a $outdir/soapdenovo/kmer.$kmer[$t]/out.scafSeq -o $outdir/soapdenovo/kmer.$kmer[$t]/out2.scafSeq -t 8 -p 31\n";
                $soap_contig .="$outdir/soapdenovo/kmer.$kmer[$t]/out2.scafSeq ";
            }
            else
            {
                $soap_contig .="$outdir/soapdenovo/kmer.$kmer[$t]/out2.scafSeq ";
            }
        }
system "perl $qsub --ppn $cpu --queue $queue $outdir/soapdenovo_1.sh";
system "perl $qsub $outdir/gapcloser_2.sh";
##############################################output assembly stat
system "mkdir -p $outdir/quast";
system "cd $outdir/soapdenovo/ && $python $quast  --no-html --plots-format png --contig-thresholds 0,500,1000,10000,100000,1000000,10000000 --no-check -o  $outdir/quast $soap_contig";
