#!/local_data1/software/perl/perl-v5.28.0/bin/perl
use strict;
use warnings;
use FindBin qw($Bin);
use Getopt::Long;
use Cwd;
use Cwd 'abs_path';
my $Rscript="/local_data1/software/R/R-v3.4.0/bin/Rscript";
my($gtf,$lncRNA,$outdir,$mRNA);
$outdir||=getcwd;

GetOptions(
    "l:s"=>\$lncRNA,       
    "g:s"=>\$gtf,       
    "m:s"=>\$mRNA,
    "o:s"=>\$outdir,
           );
sub usage{
    print qq{
This script will compare mRNA and LncRNA.

options:
-l      lncRNA fasta sequence
-m      mRNA fasta sequence
-g      gtf file
-o      output directory

Email:fanyucai1\@126.com
2018.9
    };
    exit;
}
if(!$lncRNA ||!$mRNA||!$gtf)
{
    &usage();
}
$outdir=abs_path($outdir);
$lncRNA=abs_path($lncRNA);
$mRNA=abs_path($mRNA);
my (%trans,%lhash,%mhash,$ID);
open(TR,"$gtf");
while(<TR>)
{
    chomp;
    if($_!~/^#/)
    {
        my @array=split(/\t/,$_);
        if($array[8]=~/transcript_id \"(\S+)\";/)
        {
            $ID=$1;
        }
        if($array[8]=~/exon_number \"(\S+)\";/)
        {
            $trans{$ID}=$1;
        }
    }
}
my(%len1,%len2);
open(LN,"$lncRNA");
while(<LN>)
{
    chomp;
    if($_=~/\>/)
    {
        $ID=substr($_,1);
        if($trans{$ID}>=10)
        {
            $lhash{10}++;
        }
        else
        {
            $lhash{$trans{$ID}}++;
        }
    }
    else
    {
        $len1{$ID}.=$_;
    }
}
open(MR,"$mRNA");
while(<MR>)
{
    chomp;
    if($_=~/\>/)
    {
        $ID=substr($_,1);
        if($trans{$ID}>=10)
        {
            $mhash{10}++;
        }
        else
        {
            $mhash{$trans{$ID}}++;
        }
    }
    else
    {
        $len2{$ID}.=$_;
    }
}
open(LEN,">$outdir/length_dis.txt");
print LEN "Type\tLength\n";
foreach my $key(keys %len1)
{
    print LEN "LncRNA","\t",length($len1{$key}),"\n";
}
foreach my $key(keys %len2)
{
    print LEN "mRNA","\t",length($len2{$key}),"\n";
}
open(EXON,">$outdir/exon_num.txt");
print EXON "Exon_num\tcounts\tType\n";
for(my $i=1;$i<=10;$i++)
{
    if(exists $lhash{$i})
    {
        print EXON "$i\t$lhash{$i}\tlncRNA\n";
    }
    else
    {
        print EXON "$i\t0\tlncRNA\n";
    }
    if(exists $mhash{$i})
    {
        print EXON "$i\t$mhash{$i}\tmRNA\n";
    }
    else
    {
        print EXON "$i\t0\tmRNA\n";
    }
}
##############################
system "echo '#!$Rscript
library(ggplot2)
x=read.table(\"$outdir/exon_num.txt\",sep=\"\\t\",header=T)
p=ggplot(data=x,aes(x=Exon_num,y=counts,fill=Type))+geom_bar(stat=\"identity\",position=position_dodge())+scale_x_continuous(breaks=seq(1,11,1))
pdf(\"$outdir/exon_num.pdf\",width=10,height=10)
p
dev.off()
m=read.table(\"$outdir/length_dis.txt\",sep=\"\\t\",header=T)
p=ggplot(data=m,aes(x=Length,fill=Type))+geom_density()
pdf(\"$outdir/length_dis.pdf\",width=10,height=10)
p
dev.off()
'>$outdir/lncRNA_mRNA.Rscript
";

system "$Rscript $outdir/lncRNA_mRNA.Rscript";
