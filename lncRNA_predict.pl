#!/local_data1/software/perl/perl-v5.28.0/bin/perl
use strict;
use warnings;
use FindBin qw($Bin);
use Cwd;
use Cwd 'abs_path';
use Getopt::Long;

my $perl="/local_data1/software/perl/perl-v5.28.0/bin/perl";
my $hmmer3="/local_data1/software/hmmer/hmmer-3.1b1/bin/";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my $pfam="/local_data1/reference/Pfam/Pfam32.0/";
my $python="/local_data1/software/python/python-v2.7.9/bin/python";
my $cpc2="/local_data1/software/CPC/CPC2-beta/bin/CPC2.py";
my $CNCI="/local_data1/software/CNCI/CNCI-master/CNCI.py";
my $PLEK="/local_data1/software/PLEK/PLEK.1.2/PLEK.py";
my $Rscript="/local_data1/software/R/R-v3.4.0/bin/Rscript";
my $rfamscan="/local_data1/reference/Rfam/Rfam_11.0/rfam_scan.pl";
my $infernal_blast="export PATH=/local_data1/software/blast/blast-2.2.26/bin/:/local_data1/software/Infernal/infernal-v1.0.2/bin:\$PATH";
my $db_rfam="/local_data1/reference/Rfam/Rfam_11.0/";
my $transdecoder="/local_data1/software/TransDecoder/TransDecoder-TransDecoder-v5.3.0/TransDecoder.LongOrfs";

my($outdir,$prefix,$model,$fa,$gtf);
$outdir=getcwd;
GetOptions(
    "fa:s"=>\$fa,
    "p:s"=>\$prefix,
    "o:s"=>\$outdir,
    "m:s"=>\$model,
    "g:s"=>\$gtf,
           );
sub usage{
    print qq{
This script will use pfamscan+CNCI+cpc2+PLEK to predict lncRNA. 
options:
-fa     input fasta files(force)
-p      output of prefix(force)
-o      output directory(default:$outdir)
-g      gtf file from stringtie output(force)
-m      assign the classification models ("ve" for vertebrate species, "pl" for plat species):force
Email:fanyucai1\@126.com
2018.8.16
    };
    exit;
}
if(!$prefix||!$model)
{
    &usage();
}
system "mkdir -p $outdir";
$fa=abs_path($fa);
open(TR,"$fa");
my ($ID,%seq,%mRNA);
while(<TR>)
{
    chomp;
    if($_=~/\>/)
    {
        $ID=substr($_,1);
    }
    else
    {
        $seq{$ID}.=$_;
        $mRNA{$ID}.=$_;
    }
}
##################################################################################filter one exon and length <200
my(%exon);
open(GTF,$gtf);
while(<GTF>)
{
    chomp;
    if($_!~/#/)
    {
        my @array=split(/\t/,$_);
        if($array[8]=~/transcript_id "(\S+)";/)
        {
                $ID=$1;
        }
        if($array[8]=~/exon_number \"(\S+)\";/)
        {
                $exon{$ID}=$1;
        }
    }
}
open(OUT,">$outdir/lnc_pre.fasta");
foreach my $key(keys %seq)
{
    if($exon{$key} ne "1")
    {
        if(length($seq{$key})>=200)
        {
            print OUT ">$key\n$seq{$key}\n";
        }
        else
        {
            $seq{$key}=1;
        }
    }
    else
    {
            $seq{$key}=1;
    }
}
$fa="$outdir/lnc_pre.fasta";
###################################################################################pfam+cpc2+PLEK+CNCI
my (%hash1,%hash2,%hash3,%hash4);
open(SH,">$outdir/LncRNA.sh");
print SH "cd $outdir && $transdecoder -t $fa -S && ";#https://github.com/TransDecoder/TransDecoder/wiki
print SH "$hmmer3/hmmscan --cpu 30 -E 0.001 --domtblout $outdir/$prefix.pfam.domtblout $pfam/Pfam-A.hmm $fa.transdecoder_dir/longest_orfs.pep\n";
if(! -e "$outdir/$prefix.cpc2.out")
{
    print SH "$python $cpc2 -i $fa -o $outdir/$prefix.cpc2.out\n";
}
if(! -e "$outdir/$prefix/CNCI.index")
{
    print SH "$python $CNCI -f $fa -p 20 -o $outdir/$prefix -m $model\n";#output CNCI.index
}
if(! -e "$outdir/$prefix.PLEK.out")
{
    print SH "$python $PLEK -fasta $fa -thread 20 -out $outdir/$prefix.PLEK.out\n";
}
if(! -e "$outdir/$prefix.pfam.domtblout")
{
    system "perl $qsub $outdir/LncRNA.sh";
}
###################################################################################parse cpc2 output
open(IN1,"$outdir/$prefix.cpc2.out");
while(<IN1>)
{
    chomp;
    if($_!~/^#/)
    {
        my @array=split;
        if($array[$#array] =~ "noncoding")
        {
            $hash1{$array[0]}=1;
        }
    }
}
#####################################################################################parse PLEK out
open(IN2,"$outdir/$prefix.PLEK.out");
while(<IN2>)
{
    chomp;
    my @array=split;
    if($array[0] =~ "Non-coding")
    {
        $hash2{substr($array[$#array],1)}=1;
    }
}
#####################################################################################parse CNCI out
open(IN3,"$outdir/$prefix/CNCI.index");
while(<IN3>)
{
    chomp;
    if($_=~/noncoding/)
    {
        my @array=split;
        $hash3{$array[0]}=1;
    }
}
#######################################################################################parse pfam out
open(IN4,"$outdir/$prefix.pfam.domtblout");

while(<IN4>)
{
    chomp;
    my $ID;
    if($_!~/^#/ && $_=~/PF/i)
    {
        my @array=split;
        my @array1=split(/\./,$array[3]);
        for(my $i=0;$i<$#array1;$i++)
        {
            if($i==0)
            {
                $ID=substr($array1[0],1);
            }
            else
            {
                $ID.=".$array[$i]"; 
            }
        }
        $seq{$ID}=1;  
    }
}
foreach my $key(keys %seq)
{
    if($seq{$key} ne "1")
    {
        $hash4{$key}=1;   
    }
}
###############################################################################################plot venn
my ($a,$ab,$ac,$ad,$abc,$acd,$abd,$abcd);
open(OUT,">$outdir/lncRNA.fa");
foreach my $key(keys %hash1)
{
    $a++;
    if(exists $hash2{$key})
    {
        $ab++;
    }
    if(exists $hash3{$key})
    {
        $ac++;
    }
    if(exists $hash4{$key})
    {
        $ad++;
    }
    if(exists $hash2{$key} && exists $hash3{$key})
    {
        $abc++;
    }
    if(exists $hash2{$key} && exists $hash4{$key})
    {
        $abd++;
        
    }
    if(exists $hash3{$key} && exists $hash4{$key})
    {
        $acd++;
    }
    if(exists $hash2{$key} && exists $hash3{$key} && exists $hash4{$key})
    {
        $abcd++;
        print OUT ">$key\n$mRNA{$key}\n";
    }
}
my($b,$bc,$bd,$bcd);
foreach my $key(keys %hash2)
{
    $b++;
    if(exists $hash3{$key})
    {
        $bc++;
        if(exists $hash4{$key})
        {
            $bcd++;
        }  
    }
    if(exists $hash4{$key})
    {
        $bd++;
    }
    
}
my($c,$cd);
foreach my $key(keys %hash3)
{
    $c++;
    if(exists $hash4{$key})
    {
        $cd++;
    }
}
my $d;
foreach my $key(keys %hash4)
{
    $d++;
}
system "echo '
#!$Rscript
library(VennDiagram)
venn.plot<-draw.quad.venn(area1=$a,area2=$b,area3=$c,area4=$d,n12=$ab,n14=$ad,n23=$bc,n24=$bd,n13=$ac,n123=$abc,n124=$abd,n134=$acd,n234=$bcd,n34=$cd,n1234=$abcd,category = c(\"CPC2\", \"PLEK\", \"CNCI\",\"Pfam\"),fill = c(\"orange\",\"blue\", \"red\", \"green\"),lty = \"blank\",cat.col = c(\"orange\",\"blue\", \"red\", \"green\"))
pdf(\"$outdir/lncRNA_venn.pdf\",width=10,height=10)
grid.draw(venn.plot);
dev.off();
'>$outdir/cpc_plek_CNCI.R";
system "$Rscript $outdir/cpc_plek_CNCI.R && rm $outdir/cpc_plek_CNCI.R";
##################################################################################anno lncRNA using Rfam
system "echo '$infernal_blast && $perl $rfamscan -blastdb $db_rfam/Rfam.fasta $db_rfam/Rfam.cm $outdir/lncRNA.fa -o $outdir/$prefix.rfam.out'>$outdir/Rfam.sh";
if(! -e "$outdir/$prefix.rfam.out")
{
    system "perl $qsub $outdir/Rfam.sh";
}
open(RFM,"$outdir/$prefix.rfam.out");#filter re-microRNA, tRNA, rRNA, and snoRNA
while(<RFM>)
{
    chomp;
    if($_!~/#/)
    {
        my @array=split;
        if($_=~/rfam-id=tRNA/)
        {
            $mRNA{$array[0]}=1;
        }
        if($_=~/rfam-id=sno/)
        {
            $mRNA{$array[0]}=1;
        }
        if($_=~/rRNA/)
        {
            $mRNA{$array[0]}=1;
        }
        if($_=~/rfam-id=MIR/ || $_=~/rfam-id=mir/)
        {
            $mRNA{$array[0]}=1;
        }
    }
}
##########################################################################################get mRNA and lncRNA FASTA SEQUENCE
system "rm -rf $outdir/lncRNA.fa";
open(MR,">$outdir/mRNA.fa");
open(OUT,">$outdir/lncRNA.fa");
foreach my $key(keys %mRNA)
{
    if($mRNA{$key} ne "1")
    {
        if(exists $hash1{$key} && exists $hash2{$key} && exists $hash3{$key} && exists $hash4{$key})
        {
            print OUT ">$key\n$mRNA{$key}\n";
        }
        else
        {
            print MR ">$key\n$mRNA{$key}\n";
        }
    }
}