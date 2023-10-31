#!/usr/bin/perl -w
use strict;
use warnings;
use FindBin qw($Bin);
use Getopt::Long;
use Cwd;
use File::Basename;

my $config="[DEFAULT]\nkobas_home =/home/fanyucai/software/kobas/kobas-3.0\nblast_home =/home/fanyucai/software/blast+/ncbi-blast-2.6.0+/bin/\n";
$config.="[KOBAS]\nkobasdb =/home/fanyucai/software/kobas/kobas-3.0/sqlite3/\ngmt =/home/fanyucai/software/kobas/kobas-3.0/gmt/\ngrn =/home/fanyucai/software/kobas/kobas-3.0/grn/\nmodel =/home/fanyucai/software/kobas/kobas-3.0/model/\n";
$config.="[BLAST]\nblastp =/home/fanyucai/software/blast+/ncbi-blast-2.6.0+/bin/blastp\nblastx =/home/fanyucai/software/blast+/ncbi-blast-2.6.0+/bin/blastx\nblastdb =/home/fanyucai/software/kobas/kobas-3.0/seq_pep/\n";

my $kobas_script="/home/fanyucai/software/kobas/kobas-3.0/scripts/";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my $python="/home/fanyucai/software/python/Python-v2.7.9/bin/python";
my $db="/public/land/database/KEGG.2018.3.15";
my $R="/home/fanyucai/software/R/R-v3.2.0/bin/Rscript";
my ($outdir,$species,$type,$input,$del);
$outdir||=getcwd;
$species||="ko";
$type||="fasta:nuc";
$del||="true";
GetOptions(
    "i:s"=>\$input,
    "o:s"=>\$outdir,
    "t:s"=>\$type,
    "sp:s"=>\$species,
    "d:s"=>\$del,
           );
sub usage{
    print qq{
This script will run kobas to annotate the KEGG.
usage:
perl $0  -i input -o $outdir -t fasta:nuc -sp ko -d t

options:
-i      input data file
-sp     species abbreviation (default:ko)
-t      input type (fasta:pro, fasta:nuc, blastout:xml,blastout:tab, id:ncbigi, id:uniprot, id:ensembl,id:ncbigene), default fasta:nuc
-d      not analysis Human Diseases(default:true) or false
-o      output directory(default:$outdir)

     
Email:fanyucai1\@126.com
2018.3.20
    };
    exit;
}
if(!$input||!$type||!$species)
{
    &usage();
}
########################################mkdir output directory
system "mkdir -p $outdir/shell/";
#########################################kobas and convert env
my $user=`whoami`;
chomp($user);
system "rm -rf $outdir/png/ && mkdir -p $outdir/png/";
if(! -e "/home/$user/.kobasrc")
{
    open(RC,">/home/$user/.kobasrc");
    print RC $config;
}
if(!-e "/home/$user/.config/ImageMagick")
{
    system "mkdir -p /home/$user/.config/ImageMagick";
    system "cp /home/fanyucai/.config/ImageMagick/* /home/$user/.config/ImageMagick/";
}
my $convert="/home/fanyucai/lib/usr/bin/convert";
my $env="export LD_LIBRARY_PATH=/home/fanyucai/lib/usr/lib64/:\$LD_LIBRARY_PATH && ";
$env.="export MAGICK_CONFIGURE_PATH=/home/$user/.config/ImageMagick && ";
$env.="export MAGICK_CODER_MODULE_PATH=/home/fanyucai/lib/usr/lib64/ImageMagick-6.7.2/modules-Q16/coders && ";
###########################################run kobas
open(KOBAS,">$outdir/shell/annotate.sh");
print KOBAS "$python $kobas_script/annotate.py -i $input -t $type -s $species -n 20 -o $outdir/kobas.out\n";
system "perl $qsub $outdir/shell/annotate.sh";
############################################parse kobas
open(KO,"$outdir/kobas.out");
my (%gene,%geneID,%query,%gene2ko,$tgene,%geneID2ko,%ko,$name);
while(<KO>)
{
    chomp;
    if($_!~"#" && $_!~/None/ && $_ ne "")
    {
        my @array=split(/\t/,$_);
        if($#array==1)
        {
            my @array1=split(/\|/,$array[1]);
            if($#array1==2)
            {
                $array1[0]=~s/^\s+|\s+$//;
                $array1[1]=~s/^\s+|\s+$//;
                $array1[2]=~s/^\s+|\s+$//;
                $gene{$array[0]}=$_;
                $geneID{$array1[0]}=$array1[0];
                $query{$array[0]}=$array1[0];#query2geneID
            }
        }
        if($_ =~ /^Gene:/)
        {
            if($array[1]=~/[a-zA-Z0-9]/)
            {
                $array[1]=~s/^\s+|\s+$//;
                $tgene=$array[1];
            }
        }
        if($_=~/^Query:/)
        {
            if($array[1]=~/[a-zA-Z0-9]/)
            {
                $array[1]=~s/^\s+|\s+$//;
                $name=$array[1];
            }
        }
        if($_=~/\s+KEGG PATHWAY\s+[A-za-z]+([0-9]+)/)
        {
                my $string="ko";
                $string.=$1;
                $geneID2ko{$name}{$tgene}.="$string|";#GeneID2ko
                $ko{$string}=1;
        }
    }
}
##############################################################get all KO description
open(DES,"$db/KO_des/KO_des.txt");
my(%des);
while(<DES>)
{
    chomp;
    my @array=split;
    my @array1=split(/;/,$_);
    $array1[1]=~s/^\s+|\s+$//;
    $des{substr($array[0],3)}=$array1[1];#KO2descript
}
#############################################################get species KO number
my ($dir,%KO,%hash);
if($species eq "ko")
{
   $dir="$db/$species.txt";
}
else
{
   $dir="$db/gene2KO/$species.txt";
}
open(DB,"$dir");
while(<DB>)
{
    chomp;
    my @array=split(/\t/,$_);
    $array[0]=~s/^\s+|\s+$//;
    $array[1]=~s/^\s+|\s+$//;
    $array[1]=substr($array[1],3);
    if(exists $geneID{$array[0]})
    {
        $hash{$array[0]}{$array[1]}=$des{$array[1]};#{geneID}{KO}=descript
        $KO{$array[1]}=1;
    }
}
#############################################################get colour KEGG png
my @html=glob("$db/ko/*html");
open(CN,">$outdir/convert.sh");
my (%KO2ko,$j,$ko_num,$png);
PO:foreach my $key(@html)
{
    $ko_num=basename $key;
    $ko_num=~s/.html//;
    if(exists $ko{$ko_num})
    {
        $png=$key;
        $png=~s/html$/png/;
        $j++;
        system "cp $png $outdir/png/";
    }
    else
    {
        next PO;
    }
}
foreach my $key(keys %geneID2ko)
{
    foreach my $key1(keys %{$geneID2ko{$key}})
    {
        my @koID=split(/\|/,$geneID2ko{$key}{$key1});
        foreach my $num(@koID)
        {
            print $num,"\n";
            if(-e "$db/ko/$num.html")
            {
                open(HTML,"$db/ko/$num.html");
                while(<HTML>)
                {
                    chomp;
                    my @array;
                    if($_=~/title=\"(K.*)\"/)#获取KO号码以及基因名字
                    {
                        @array=split(/\,/,$1);
                    }
                    if($_=~/shape=(rect|poly)\s+coords=([0-9,]+)/)#获取坐标
                    {
                        my $type=$1;
                        my @coords=split(",",$2);
                        foreach my $key(@array)
                        {
                            if($key=~/(\S+)\s+\((\S+)\)/)
                            {
                                if(exists $hash{$key1}{$1})
                                {
                                    if($type eq "rect")
                                    {
                                        my $c="46x18+$coords[0]+$coords[1]";
                                        print CN "$env && $convert $outdir/png/$num.png -fuzz 80% -fill lightgreen -region $c -opaque white $outdir/png/$num.png\n";
                                    }
                                    if($type eq "poly")
                                    {
                                        my $c="line $coords[0],$coords[1] $coords[2],$coords[3]";
                                        print CN "$env && $convert $outdir/png/$num.png -stroke lightgreen -strokewidth 2 -draw \"$c\" $outdir/png/$num.png\n";
                                    }
                                }
                            }
                        }
                    }
                }
            }
       
        }
    }
}
#system "perl $qsub --lines 20 --maxproc 20 --ppn 2 $outdir/convert.sh";
########################################################get KEGG stastics
open(MA,"$db/KEGGpathway_three_levels_v2.txt");
my (%class1,%class2,%class3,%counts);
while(<MA>)
{
    chomp;
    my @array=split(/\;/,$_);
    $array[3]=~s/^\s+|\s+$//;
    if($del=~/t/i)
    {
        if($array[1]!~/human/i)
        {
            $class1{$array[0]}=$array[1];
            $class2{$array[0]}=$array[2];
            $class3{$array[0]}="$array[0]|$array[3];";
        }
    }
    else
    {
        $class1{$array[0]}=$array[1];
        $class2{$array[0]}=$array[2];
        $class3{$array[0]}="$array[0]|$array[3];";
    }
  
}
##############################################################output annotate result
open(OUT,">$outdir/kegg_anno.xls");
print OUT "#Query\tGene_ID|Gene_name|Hyperlink\tKO|Definition\tPathway\n";
foreach my $key(keys %gene)
{
    print OUT $gene{$key},"\t";
    foreach my $KO (keys %{$hash{$query{$key}}})
    {
        $hash{$query{$key}}{$KO}=~s/^\s+|\s+$//;
        print OUT $KO,"|",$hash{$query{$key}}{$KO},";";
    }
    print OUT "\t";
    if(exists $geneID2ko{$key}{$query{$key}})
    {
        my @koID=split(/\|/,$geneID2ko{$key}{$query{$key}});
        foreach my $key1 (@koID)
        {
            if($key1 !~/\s+/ && exists $class3{$key1})
            {
                $counts{$class1{$key1}}{$class2{$key1}}++;
                print OUT "$class3{$key1}";
            }
        }
    }
    print OUT "\n";
}
###############################################pathway counts
open(COUNT,">$outdir/counts.txt");
print COUNT "Pathway\tCounts\tClassify\n";
foreach my $key (keys %counts)
{
    foreach my $key1(keys %{$counts{$key}})
    {
        print COUNT "$key1\t$counts{$key}{$key1}\t$key\n";
    }
}
############################################plot counts
open(BAR,">$outdir/bar.Rscript");
print BAR "#!$R
library(ggplot2)
x=read.table(\"$outdir/counts.txt\",sep=\"\\t\",header=T)
p=ggplot(x,aes(x=factor(Pathway,order=T,levels=Pathway),y=Counts,fill=Classify))+ geom_bar(stat=\"identity\")+xlab(\"Pathway\")+ylab(\"Counts of Genes\")+coord_flip()+geom_text(aes(label=Counts),position = position_dodge(0.9), vjust = 0,size=2)
p=p+ggtitle(\"KEGG Classification\")
p=p+theme(legend.text = element_text(size=6),legend.title=element_blank(),axis.text= element_text(size=5),axis.title = element_text(size=7),plot.title = element_text(size=8))
png(\"$outdir/kegg_bar.png\",res=300,width=2400,height=1200)
p
dev.off()
pdf(\"$outdir/kegg_bar.pdf\",width=15,height=10)
p
dev.off()
";
system "$R $outdir/bar.Rscript && rm $outdir/bar.Rscript";
