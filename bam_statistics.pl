#!/usr/bin/perl -w
use strict;
use warnings;
use Getopt::Long;
use Cwd;
my (@bam,$outdir,@prefix,$genomeSize,$bed);
my $R="/data02/software/R/R-v3.5.0/bin/Rscript";
my $samtools="/data02/software/samtools/samtools-1.9//samtools";
my $picard="/data02/software/picard/picard.jar";
my $bedtools="/data02/software/bedtools/bedtools2/bin/bedtools";
my $inner_distance="/data02/software/python/Python-v3.7.0/bin/inner_distance.py";
my $python="/data02/software/python/Python-v3.7.0/bin/python3";
my $geneBody_coverage="/data02/software/python/Python-v3.7.0/bin/geneBody_coverage.py";
my $RPKM_saturation="/data02/software/python/Python-v3.7.0/bin/RPKM_saturation.py";
my $junction_saturation="/data02/software/python/Python-v3.7.0/bin/junction_saturation.py";
my $GC="/data02/software/python/Python-v3.7.0/bin/read_GC.py";
my $window||=10000;
my $readlength||=150;
GetOptions(
    "bam:s{1,}"=>\@bam,
    "o:s"=>\$outdir,
    "p:s{1,}"=>\@prefix,
    "genomeSize:s"=>\$genomeSize,
    "w:s"=>\$window,
    "bed:s"=>\$bed,
    "r:s"=>\$readlength,
           );

sub usage{
    print qq{
This script plot barplot with mapped/unmapped reads,insert length,chromosome coverage.
Attention:As the analysis of without_RNAseq,the bam file will not delet dumplicate.

usage:
perl $0 -bam sample1.bam sample2.bam -o /path/to/outdir -p sample1 sample2  -w 10000 -genomeSize genome.fa.fai
                    or
perl $0 -bam sample1.bam sample2.bam -o /path/to/outdir -p sample1 sample2
                    or
perl $0 -bam sample1.bam sample2.bam -o /path/to/outdir -p sample1 sample2 -bed ###.gtf.bed

options:
-bam            input file,you could input several files and split by space(force)
-genomeSize     input bed file contains chromosome size this file from samtools faidx ouput(force)
-bed            the bed file from transdecoder(will plot rand curve and saturation curve.)
-w              the silde window(default:10000)
-o              the out directory
-p              the prefix of output,corresponding the input(force)
-r		read length(default:150,force)

Email:fanyucai1\@126.com
2018.12.24
    };
    exit;
}
if (!@bam || !$outdir || !@prefix)
{
    &usage();
}
my($pdfw,$pdfh,$pngw,$pngh);
if($#bam<5)
{
   $pdfw=8;
   $pdfh=8;
   $pngw=1000;
   $pngh=1000;
}
else
{
   $pdfw=10;
   $pdfh=10;
   $pngw=2000;
   $pngh=2000;
}
######plot mapping ratio
my ($mapped,$unmapped,$total);
system "mkdir -p $outdir/";
system "echo 'SampleID\tTotal\tMapped\tUnmapped\tMapped_Ratio(%)' >$outdir/mapped_stat.xls";
for (my $i=0;$i<=$#bam;$i++)
{
    `$samtools flagstat -@ 20 $bam[$i] >$outdir/flagstat.txt`;
    `$python3 $GC -i $bam[$i] -o $outdir/$prefix[$i].GC`;
    open(TM,"$outdir/flagstat.txt");
    while(<TM>)
    {
	chomp;
	my @array=split;
	if($_=~/paired in sequencing/)
	{
		$total=$array[0];
	}
	if($_=~/properly paired/)
	{
		$mapped=$array[0];
	}
    }
    $unmapped=$total-$mapped;
    my $ratio=$mapped/$total;
    system "echo '$prefix[$i]\t$total\t$mapped\t$unmapped\t$ratio' >>$outdir/mapped_stat.xls";
    `java -jar $picard CollectInsertSizeMetrics I=$bam[$i]  H=$outdir/$prefix[$i]\_insert_size_histogram.pdf O=$outdir/$prefix[$i]\_insert_size_metrics.txt`;
    open(IN,"$outdir/$prefix[$i]\_insert_size_metrics.txt");
    my $num=0;
    TT:while (<IN>)
    {
        chomp;
        if ($_ =~"All_Reads.fr_count")
        {
            ++$num;
            system "echo $_ >$outdir/$prefix[$i]\_insert_size.txt";
            next TT;
        }
        if ($num==1)
        {
            system "echo $_ >>$outdir/$prefix[$i]\_insert_size.txt";
        }  
    }
    close;
}
`rm $outdir/flagstat.txt && rm $outdir/*insert_size_histogram.pdf`;
#################################################plot mapping ratio
system "echo '#!$R'>$outdir/map_stat.R";
system "echo '
library(ggplot2)
library(reshape2)
library(plyr)
ReadCount<-read.table(\"$outdir/mapped_stat.xls\",header=T)            
ReadCountSmall <- data.frame(sampleID= ReadCount\$SampleID, Mapped = ReadCount\$Mapped, Unmapped = ReadCount\$Unmapped)
MeltedReadCount = melt(ReadCountSmall)
ReadsFraction <- ddply(MeltedReadCount,.(sampleID),summarise,Count.Fraction = value / sum(value))
to_graph <- cbind(arrange(MeltedReadCount, sampleID), fraction = ReadsFraction\$Count.Fraction)
gp <- ggplot(data=to_graph, aes(x=sampleID, y=value, fill=variable)) +geom_bar(stat=\"identity\",position = \"stack\") +labs(y=\"reads count\")+
geom_text(aes(label=paste(round(fraction*100),\"%\", sep=\"\")),size = 2,vjust=0,position=\"stack\") +theme(axis.text.x=element_text(angle=90))
pdf(\"$outdir/MappedReads.pdf\",width=$pdfw,height=$pdfh)
gp
dev.off()
png(\"$outdir/MappedReads.png\",res=300,width=$pngw,height=$pngh)
gp
dev.off()
'>>$outdir/map_stat.R";
system "$R $outdir/map_stat.R && rm $outdir/map_stat.R";
######################################plot insert length
system "echo '#!$R'>$outdir/plot.insert.R";
for(my $i=0;$i<=$#bam;$i++)
{
   system "echo 'a<-read.table(\"$outdir/$prefix[$i]\_insert_size.txt\",header=T)'>>$outdir/plot.insert.R";
   system "echo 'x<-a\$insert_size'>>$outdir/plot.insert.R";
   system "echo 'y<-a\$All_Reads.fr_count'>>$outdir/plot.insert.R";
   system "echo 'png(filename=\"$outdir/$prefix[$i].insert_length.png\",res=300,width=$pngw,height=$pngh)'>>$outdir/plot.insert.R";
   system "echo 'plot(spline(x,y), pch=20,xlab=\"Insert size\", ylab=\"reads number\", lwd=2,type=\"l\", main=paste(\"Insert size distribution\"),col=2)'>>$outdir/plot.insert.R";
   system "echo 'dev.off()'>>$outdir/plot.insert.R";
   system "echo 'pdf(file=\"$outdir/$prefix[$i].insert_length.pdf\",width=$pdfw,height=$pdfh)'>>$outdir/plot.insert.R";
   system "echo 'plot(spline(x,y), pch=20,xlab=\"Insert size\", ylab=\"reads number\", lwd=2,type=\"l\", main=paste(\"Insert size distribution\"),col=2)'>>$outdir/plot.insert.R";
   system "echo 'dev.off()'>>$outdir/plot.insert.R";
}
system "$R $outdir/plot.insert.R && rm $outdir/plot.insert.R $outdir/*insert_size.txt";
######################################plot sequencing coverage based on bam files
if($window && $genomeSize)
{
    system "$bedtools makewindows -g $genomeSize -w $window >$outdir/ref.$window.bed";
    system "echo '#!$R'>$outdir/plot_per_chrom_cov.R";
    open(IN,"$outdir/ref.$window.bed");
    open(OUT,">$outdir/ref.$window\_chr.bed");
    while (<IN>)
    {
        chomp;
        if ($_=~"chr" || $_=~/^[1-9]/)
        {
                print OUT "$_\n";
        }
    }
    for(my $i=0;$i<=$#bam;$i++)
    {
        system "$samtools bedcov -Q 10 $outdir/ref.$window\_chr.bed $bam[$i] >$outdir/$prefix[$i].$window.cov";
        system "echo 'x<-read.table(\"$outdir/$prefix[$i].$window.cov\")'>>$outdir/plot_per_chrom_cov.R";
        system "echo 'chr<-x[,1]'>>$outdir/plot_per_chrom_cov.R";
        system "echo 'pos<-x[,3]'>>$outdir/plot_per_chrom_cov.R";
        system "echo 'depth<-x[,4]*$readlength/$window'>>$outdir/plot_per_chrom_cov.R";
        system "echo 'df  <- data.frame(chr, pos, depth)'>>$outdir/plot_per_chrom_cov.R";
        system "echo 'require(ggplot2)'>>$outdir/plot_per_chrom_cov.R";
        system "echo 'pdf(file=\"$outdir/$prefix[$i]\_cov.pdf\",width=40,height=30)'>>$outdir/plot_per_chrom_cov.R";
        system "echo 'p <- ggplot(data = df, aes(x=pos, y=depth),binwidth = 0.1) + geom_area(aes(fill=chr))'>>$outdir/plot_per_chrom_cov.R";
        system "echo 'p + facet_wrap(~ chr, ncol=1)'>>$outdir/plot_per_chrom_cov.R";
        system "echo 'dev.off()'>>$outdir/plot_per_chrom_cov.R";
        system "echo 'png(filename=\"$outdir/$prefix[$i]\_cov.png\",width=6000,res=300,height=5000)'>>$outdir/plot_per_chrom_cov.R";
        system "echo 'p <- ggplot(data = df, aes(x=pos, y=depth),binwidth = 0.1) + geom_area(aes(fill=chr))'>>$outdir/plot_per_chrom_cov.R";
        system "echo 'p + facet_wrap(~ chr, ncol=1)'>>$outdir/plot_per_chrom_cov.R";
        system "echo 'dev.off()'>>$outdir/plot_per_chrom_cov.R";
    }
    system "$R $outdir/plot_per_chrom_cov.R && rm $outdir/plot_per_chrom_cov.R";
}

if($bed)
{
    for(my $i=0;$i<=$#bam;$i++)
    {
        system "$python $RPKM_saturation -r $bed -i $outdir/$bam[$i] -o $outdir/$prefix[$i]\.saturation_curve";
        system "$python $geneBody_coverage -r $bed -i $outdir/$bam[$i] -o $outdir/$prefix[$i]\.rand";
        system "$python $junction_saturation -r $bed -i $outdir/$bam[$i] -o $outdir/$prefix[$i]\.junction_saturation";
    }
}
