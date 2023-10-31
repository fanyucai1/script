#!/usr/bin/perl env
use strict;
use warnings;
use File::Basename;
use File::Spec;
use Getopt::Long;
use FindBin qw($Bin);

#############################################################################
my $env="export PATH=/home/fanyucai/software/gcc/gcc-v6.1.0/bin/:/home/fanyucai/software/R/R-v3.4.0/bin/:\$PATH";
$env.=" && export LD_LIBRARY_PATH=/home/fanyucai/software/gcc/gcc-v6.1.0/lib64/:\$LD_LIBRARY_PATH";
#############################################################################

my (@infile1, @infile2, @relation, @groupname, $file1name, $file2name, $file1col, $file2col, $relation_col, $outdir, $help);

GetOptions(
	"f1:s{1,}"    => \@infile1,
	"f2:s{1,}"    => \@infile2,
	"r:s{1,}"     => \@relation,
	"g:s{1,}"     => \@groupname,
	"n1:s"        => \$file1name,
	"n2:s"        => \$file2name,
	"c1:s"        => \$file1col,
	"c2:s"        => \$file2col,
	"rc:s"        => \$relation_col,
	"o:s"         => \$outdir,
	"help|h!"     => \$help,
);

my $usage=<< "USAGE";
Program: $0
Descriptions:
	-f1      <file>        The input file1, by space-delimited
	-f2      <file>        The input file2, by space-delimited
	-r       <file>        The input relation file between infile1 and infile2
	-g       <group>       The input group name, by space-delimited
	-n1      <name>        The input name of infile1
	-n2      <name>        The input name of infile2
	-c1      <str>         The infile1 id column and up_down column, format:id,up_down, eg:1,9
	-c2      <str>         The infile2 id column and up_down column, format:id,up_down, eg:1,6
	-rc      <str>         The infile1 id column and infile2 id column in relation file, eg:1,2
	-o       <dir>         The output directory of result
	-help|h                Print help infos
Example:
	perl rna_vs_rna_corr.pl -f1 A.VS.B.diff.miRNA.xls C.VS.B.diff.miRNA.xls -f2 A-vs-B-diff-pval-0.05-FC-2.gene.xls C-vs-B-diff-pval-0.05-FC-2.gene.xls -r A-vs-B.target.result.xls C-vs-B.target.result.xls -g A-vs-B C-vs-B -n1 miRNA -n2 gene -c1 1,6 -c2 1,9 -rc 1,2 -o miRNA_vs_gene_correlation_analysis/

USAGE

die $usage if(!@infile1 || !@infile2 || !@relation || !@groupname || !$file1name || !$file2name || !$file1col || !$file2col || !$relation_col || !$outdir || $help);
(@infile1==@infile2) || die "Error: file1 number isn't equal to file2 number !\n";
(@infile1==@groupname) || die "Error: infile number isn't equal to group name number !\n";
(@infile1==@relation) || die "Error: infile number isn't equal to relation file number !\n";
for(my $i=0; $i<@infile1; $i++){
	(-s $infile1[$i]) || die "Error: don't find file1: $infile1[$i] !\n";
	$infile1[$i]=File::Spec->rel2abs($infile1[$i]);
	(-s $infile2[$i]) || die "Error: don't find file2: $infile2[$i] !\n";
	$infile2[$i]=File::Spec->rel2abs($infile2[$i]);
	(-s $relation[$i]) || die "Error: don't find relation file: $relation[$i] !\n";
	$relation[$i]=File::Spec->rel2abs($relation[$i]);
}
my @file1col=split /,/,$file1col;
my @file2col=split /,/,$file2col;
my @relation_col=split /,/,$relation_col;
(-d $outdir) || mkdir $outdir;
$outdir=File::Spec->rel2abs($outdir);

for(my $i=0; $i<@infile1; $i++){
	my (%file1, %file2);
	my ($file1_head, $file2_head);

	open AA,"<$infile1[$i]" || die $!;
	while(<AA>){
		chomp;
		next if(/^\s*$/);
		my @l=split /\t/;
		my $id=$l[$file1col[0]-1];
		my $up_down=$l[$file1col[1]-1];
		next if($up_down!~/up|down/i);
		splice @l,$file1col[0]-1,1;
		if($.==1){
			$file1_head="$file1name\_id\t".join("\t",@l);
		}else{
			$file1{$id}=[$up_down, join("\t",@l)];
		}
	}
	close AA;

	open BB,"<$infile2[$i]" || die $!;
	while(<BB>){
		chomp;
		next if(/^\s*$/);
		my @l=split /\t/;
		my $id=$l[$file2col[0]-1];
		my $up_down=$l[$file2col[1]-1];
		next if($up_down!~/up|down/i);
		splice @l,$file2col[0]-1,1;
		if($.==1){
			$file2_head="$file2name\_id\t".join("\t",@l);
		}else{
			$file2{$id}=[$up_down, join("\t",@l)];
		}
	}
	close BB;

	open OUT,">$outdir/$groupname[$i]\.$file1name\_$file2name.xls" || die $!;
	print OUT "$file1_head\t$file2_head\n";
	open ES,">$outdir/$groupname[$i]\.$file1name\_$file2name.edges.xls" || die $!;
	print ES "source\ttarget\n"; my %nodes_num; my %nodes_type;
	open CC,"<$relation[$i]" || die $!;
	while(<CC>){
		chomp;
		next if(/^\s*$/ || $.==1);
		my @l=split /\t/;
		next if(!exists $file1{$l[$relation_col[0]-1]} || !exists $file2{$l[$relation_col[1]-1]});
		if(lc($file1{$l[$relation_col[0]-1]}[0]) ne lc($file2{$l[$relation_col[1]-1]}[0])){
			print OUT "$l[$relation_col[0]-1]\t$file1{$l[$relation_col[0]-1]}[1]\t$l[$relation_col[1]-1]\t$file2{$l[$relation_col[1]-1]}[1]\n";
			print ES "$l[$relation_col[0]-1]\t$l[$relation_col[1]-1]\n";
			$nodes_num{$l[$relation_col[0]-1]}++;
			$nodes_num{$l[$relation_col[1]-1]}++;
			$nodes_type{$l[$relation_col[0]-1]}="$file1name\t".lc($file1{$l[$relation_col[0]-1]}[0]);
			$nodes_type{$l[$relation_col[1]-1]}="$file2name\t".lc($file2{$l[$relation_col[1]-1]}[0]);
		}
	}
	close CC;
	close OUT;
	close ES;
	open NS,">$outdir/$groupname[$i]\.$file1name\_$file2name.nodes.xls" || die $!;
	print NS "id\tname\tup_down\tsize\n";
	for my $n(sort keys %nodes_num){
		print NS "$n\t$nodes_type{$n}\t$nodes_num{$n}\n";
	}
	close NS;
	system("$env && Rscript $Bin/network_igraph.r -e $outdir/$groupname[$i]\.$file1name\_$file2name.edges.xls -n $outdir/$groupname[$i]\.$file1name\_$file2name.nodes.xls -o $outdir/$groupname[$i]\.$file1name\_$file2name");
}

