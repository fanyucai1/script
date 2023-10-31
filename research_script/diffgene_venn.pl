#!/usr/bin/env perl
use strict;
use warnings;
use Getopt::Long;
use File::Spec;
use File::Basename;
use FindBin qw($Bin);
use Cwd;

###################### software or env ###############################################################
my $env="export PATH=/home/fanyucai/software/gcc/gcc-v6.1.0/bin/:/home/fanyucai/software/R/R-v3.4.0/bin/:\$PATH";
$env.=" && export LD_LIBRARY_PATH=/home/fanyucai/software/gcc/gcc-v6.1.0/lib64/:\$LD_LIBRARY_PATH";
######################################################################################################

my (@infile, $outdir, $annotation, $anno_colnum, $method, $help);
GetOptions(
	"i:s{1,}"   => \@infile,
	"o:s"       => \$outdir,
	"a:s"       => \$annotation,
	"c:i"       => \$anno_colnum,
	"m:s"       => \$method,
	"h|help!"   => \$help,
);

my $usage=<< "USAGE";
Program: $0
Description: draw venn graph for differentially expressed genes
Options:
	-i     <infile>    The inputfile *-vs-*-diff-*.xls                       [Required]
	-o     <outdir>    The output directory of result                        [Required]
	-a     <infile>    The input annotation.xls file                         [Optional, -a and -c can only choose one]
	-c     <num>       The starting number of columns of annotation infos    [Optional, -a and -c can only choose one]
	-m                 Draw venn graph method: VennDiagram, UpSetR           [Optional]
	                   default: VennDiagram(<=5), UpSetR(>5 && <10), Petals(>=10)
	-h|help            print help info
Example:
	perl diffgene_venn.pl -i Quantification/*-vs-*-diff-*.xls -o outdir/ -c 16
	perl diffgene_venn.pl -i Quantification/*-vs-*-diff-*.xls -o outdir/ -a annotation.xls
	perl diffgene_venn.pl -i Quantification/A-vs-B-diff-pval-0.05-FC-2.gene.xls Quantification/C-vs-B-diff-pval-0.05-FC-2.gene.xls -o outdir/ -c 16

USAGE

die $usage if(!@infile || !$outdir || $help);
die $usage if((!$annotation && !$anno_colnum) || ($annotation && $anno_colnum));
(@infile==0) && die "Error: don't find DEG file: *-vs-*-diff-*.xls !\n";
(-d $outdir) || mkdir $outdir;
$outdir=File::Spec->rel2abs($outdir);
if(defined $annotation){
	(-s $annotation) || die "Error: don't find annotation: $annotation !\n";
	$annotation=File::Spec->rel2abs($annotation);
}

for(my $i=0;$i<=$#infile;$i++){
	(-s $infile[$i]) || die "Error: don't find $infile[$i] !\n";
	$infile[$i]=File::Spec->rel2abs($infile[$i]);
}

my %diffgene; my %group;
my %anno; my $anno_header; my $id_symbol;
for my $file (@infile){
	open IN,"<$file" || die $!;
	my $filename=basename($file); $filename=~s/\.(xls|txt)$//g;
	my $group_name=(split /-diff-/, $filename)[0];
	$group{$group_name}=1;
	my $up_down_col;
	while(<IN>){
		chomp;
		next if(/^#/ || /^\s*$/);
		my @l=split /\t/;
		if($.==1){
			$id_symbol=$l[0];
			if(defined $anno_colnum){
				my $t=join("\t",@l[($anno_colnum-1)..$#l]);
				$anno_header=$t;
			}
			for my $i(2..$#l){
				if($l[$i]=~/up_down/i){
					$up_down_col=$i;
					last;
				}
			}
		}else{
			my $val=defined $up_down_col ? $l[$up_down_col] : 1;
			$diffgene{$l[0]}{$group_name}=$val;
			if(defined $anno_colnum){
				$anno{$l[0]}=join("\t",@l[($anno_colnum-1)..$#l]);
			}
		}
	}
	close IN;
}

if(defined $annotation){
	open AN,"<$annotation" || die $!;
	while(<AN>){
		chomp;
		next if(/^#/ || /^\s*$/);
		my @l=split /\t/,$_,2;
		if($.==1){
			$anno_header=$l[1];
		}else{
			$anno{$l[0]}=$l[1];
		}
	}
	close AN;
}
my @sort_group=sort keys %group;
open OUT,">$outdir/VennData.xls" || die $!;
open TMP,">$outdir/VennData_sample.xls" || die $!;
print OUT "$id_symbol\t".join("\t",@sort_group)."\t$anno_header\n";
my $temp_head=join("\t",@sort_group);
$temp_head=~s/Sample_*//ig; $temp_head=~s/Group_*//ig;
print TMP "$id_symbol\t$temp_head\n";
for my $gene (sort keys %diffgene){
	print OUT "$gene";
	print TMP "$gene";
	for my $name (@sort_group){
		if(exists $diffgene{$gene}{$name}){
			print OUT "\t$diffgene{$gene}{$name}";
			print TMP "\t1";
		}else{
			print OUT "\t0";
			print TMP "\t0";
		}
	}
	print OUT "\t$anno{$gene}\n";
	print TMP "\n";
}
close OUT;
close TMP;

######################################## draw venn graph ###############################
if(@sort_group <= 5){
	$method ||="VennDiagram";
}elsif(@sort_group > 5 && @sort_group<10){
	$method ||= "UpSetR";
}else{
	$method ||= "Petals";
}
if(@sort_group>5 && $method eq "VennDiagram"){
	die "Error: Method cannot choose VennDiagram when the data set is greater than 5 !!!\n";
}

system("perl $Bin/venn_graph.pl -i $outdir/VennData_sample.xls -f matrix -o $outdir -m $method && rm $outdir/VennData_sample.xls");

#_end_


=pod
open R,">$outdir/draw_venn.r" || die $!;
print R "#!/usr/bin/env Rscript\n";
print R "data <- read.table(\"$outdir/VennData_sample.xls\",sep=\"\\t\",header=T,quote=\"\",check.names=FALSE)\n";
if($method=~/VennDiagram/i){
	print R "InputList<-list()
mylabel=colnames(data)[-1]
for(i in 2:length(colnames(data))){
	InputList[[i-1]]<-data[which(data[,i]==1),1]
	mylabel[i-1] <- paste0(mylabel[i-1], \"\n(\", length(InputList[[i-1]]), \")\")
}
names(InputList)<-mylabel
if(length(mylabel)==2){fillColor<-c(\"red\", \"orange\")}
if(length(mylabel)==3){fillColor<-c(\"red\", \"orange\", \"green\")}
if(length(mylabel)==4){fillColor<-c(\"red\", \"orange\", \"green\", \"blue\")}
if(length(mylabel)==5){fillColor<-c(\"red\", \"orange\", \"green\", \"blue\", \"magenta\")}

library(\"VennDiagram\")
venn.plot<-venn.diagram(InputList, filename=NULL, col=NA, cat.col=\"black\", fill=fillColor, alpha =0.50, cat.cex=1.2, cat.fontface=\"bold\", margin=0.2, scale=TRUE)

pdf(file = \"$outdir/VennGraph.pdf\", width=10, height=10)
grid.draw(venn.plot)
dev.off()
png(file = \"$outdir/VennGraph.png\", width=3000, height=3000, res=300)
grid.draw(venn.plot)
dev.off()
file.remove(dir(\".\", pattern=\"^VennDiagram.*log\$\"))\n";
}elsif($method=~/UpSetR/i){
	print R "library(UpSetR)
datnum <- length(colnames(data))-1
pdf(\"$outdir/VennGraph.pdf\", width=14, height=7, onefile=F)
upset(data, nsets=datnum, nintersects=NA, number.angles=30, point.size=2, line.size=1, mainbar.y.label=\"Intersection gene number\", sets.x.label=\"Total gene number\", text.scale=c(1.3,1.3,1,1,1.3,1), mb.ratio=c(0.55, 0.45), order.by=\"freq\", show.numbers=\"yes\", sets.bar.color=rainbow(datnum))
dev.off()

png(\"$outdir/VennGraph.png\", width=4200, height=2100, res=300)
upset(data, nsets=datnum, nintersects=NA, number.angles=30, point.size=2, line.size=1, mainbar.y.label=\"Intersection gene number\", sets.x.label=\"Total gene number\", text.scale=c(1.3,1.3,1,1,1.3,1), mb.ratio=c(0.55, 0.45), order.by=\"freq\", show.numbers=\"yes\", sets.bar.color=rainbow(datnum))
dev.off()\n";
}

system("$env && Rscript $outdir/draw_venn.r && rm $outdir/VennData_sample.xls $outdir/draw_venn.r");
=cut
