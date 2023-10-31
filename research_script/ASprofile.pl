#!/local_data1/software/perl/perl-v5.28.0/bin/perl
use strict;
use warnings;
use FindBin qw($Bin);
use Getopt::Long;
use Cwd;
use Cwd 'abs_path';

my $gtf=shift;
my $outdir=shift;

my $ASprofile="/data/software/ASprofile/ASprofile.b-1.0.4";
my $Rscript="/usr/bin/Rscript";
if(!$gtf)
{
    print "usage:perl $0 text.gtf outputdirectory\n\n\n";
    exit;
}
$outdir||=getcwd;
$gtf=abs_path($gtf);
$outdir=abs_path($outdir);
system "mkdir -p $outdir";
open IN,"$gtf";
my(%chr);
while(<IN>)
{
    chomp $_;
    if($_!~/^#/)
    {
        my @col=split/\t/,$_;
        $chr{$col[0]}=1;
    }
}
open OUT,">$outdir/chr.list";
foreach my $key(keys %chr)
{
    print OUT ">$key\n";
}
open(SH,">$outdir/asprofile.sh");
print SH "$ASprofile/extract-as $gtf $outdir/chr.list >$outdir/as.out\n";
print SH "perl $ASprofile/summarize_as.pl $gtf $outdir/as.out -p $outdir/as\n";#####output as.as.nr and as.as.summary
system "sh $outdir/asprofile.sh";

open(NR,"$outdir/as.as.nr");
my (%hash,$total);
while(<NR>)
{
    chomp;
    my @array=split;
    if($_!~/event_id/ && $array[1]!~"TSS" && $array[1] !~"TTS")
    {
        $array[1]=~s/_OFF//;
        $array[1]=~s/_ON//;
        $hash{$array[1]}++;
        $total++;
    }
}
open(AS,">$outdir/as.plot.txt");
print AS "Type\tCounts\n";
foreach my $key(keys %hash)
{
    print AS "$key\t$hash{$key}\n";
}
system "echo '#!$Rscript
library(ggplot2)
x=read.table(\"$outdir/as.plot.txt\",header=T,sep=\"\\t\")
p=ggplot(data=x,aes(x=Type,y=Counts,fill=Type))+geom_bar(stat = \"identity\")+xlab(\"AS category\")+ylab(\"Number of AS\")
p=p+geom_text(aes(label=Counts),position = position_dodge(0.9), vjust = 0,size=3)

pdf(\"$outdir/AS_bar.pdf\",width=8,height=8)
p
dev.off()
'>$outdir/plot.Rscript";

system "$Rscript $outdir/plot.Rscript";