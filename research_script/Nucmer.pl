#!/home/fanyucai/software/perl/perl-v5.24.1/bin/perl
use strict;
use warnings;
use FindBin qw($Bin);
use Getopt::Long;
use File::Spec;
use Cwd;

my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my $nucmer="/home/ycliu/softwares/MUMmer3.23";
my $sample_num;
my %opts;
GetOptions(\%opts, "C=s","O=s","Q=s","h!");
$opts{O} ||= getcwd;
$opts{Q} ||= "T";
my $usage =<< "Usage";
Program:	$0

Descriptions: This script is linear alignment between reference genome and assmbly genome (software:MUMmer3.23)

Contact: qiuyu.qu\@oebiotech.com

Usage : perl $0 [options] -C config_file -O out_dir
	-C	<config_file>	input config file like:Sample	Assmbly_genome	Ref_genome(sep="\\t")
	-O	<output_dir>	output direction, this script will creat OUTDIR/Linear/sample* profile (default:./)
	-Q	<qsub or not>	delivery jobs with qsub(T) or not(F) (default:T)
	-h					print help document
	
Example perl $0 -C config.ini -O ./

Usage

die $usage if($opts{h} || ! $opts{C} );
my $outdir=File::Spec->rel2abs($opts{O});
$outdir=~s/\/$//g;
(-d "$outdir/Linear") || mkdir "$outdir/Linear";
open CONFIG,"$opts{C}";
open SH,">$outdir/Linear/Linear.sh" or die;
print SH 'export PATH=/home/fanyucai/software/gnuplot/gnuplot-V4.6.6/bin/:$PATH';
print SH "\n";
while(<CONFIG>)
{
	$sample_num+=1;
	if(/^$/){next;}
	chomp;
	my @line=split(/\t/,$_);
	my $sample_name=$line[0];
	my $asm_genome=File::Spec->rel2abs($line[1]);
	my $ref_genome=File::Spec->rel2abs($line[2]);
	(-s $ref_genome) || die "can\'t open Reference $ref_genome file!\n";
	(-s $asm_genome) || die "can\'t open Assmbly $asm_genome file!\n";
	(-d "$outdir/Linear/$sample_name") || mkdir "$outdir/Linear/$sample_name";
	print SH "\#$sample_name run code\ncd $outdir/Linear/$sample_name\n";
	print SH "$nucmer/nucmer -p $sample_name $ref_genome $asm_genome \n";
	print SH "$nucmer/mummerplot $sample_name\.delta -R $ref_genome -Q $asm_genome --filter --layout -p $sample_name -t png \n";
	print SH "$nucmer/show-snps -C $sample_name\.delta > $sample_name\.nucmer.snps \n";
	print SH "$nucmer/show-coords -r -c -l $sample_name\.delta > $sample_name\.nucmer.coords \n";
	print SH "less $sample_name\.nucmer.coords | awk '{if(NR>5)print}' | awk '{print \$1,\$2,\$4,\$5,\$7,\$8,\$10,\$12,\$13,\$15,\$16,\$18,\$19}' OFS=\"\\t\" > $sample_name\_nucmer.coords \n";
	print SH "sed -i '1i Ref_start\\tRef_end\\tQuery_start\\tQuery_end\\taligned_Ref_length\\taligned_Query_length\\tIdentity\\tRef_total_length\\tQuery_total_length\\tRef_coverage\\tQuery_coverage\\tRef_genome_ID\\tQuery_ID' $sample_name\_nucmer.coords \n";
	print SH "/home/fanyucai/software/perl/perl-v5.24.1/bin/perl /home/ycliu/softwares/All_Scripts/txt2excel.pl $sample_name\_nucmer.coords\n";
	print SH "/home/ycliu/softwares/MUMmer3.23/show-tiling $sample_name\.delta > $sample_name\.nucmer.tiling\n";
}
close CONFIG;
close SH;

##qsub
if($opts{Q} eq "T")
{
	my $all_lines=$sample_num*10+1;
	system("perl $qsub --queue all --lines $all_lines --maxproc 5 --ppn 4 $outdir/Linear/Linear.sh");
}
elsif($opts{Q} eq "F")
{
	system("bash $outdir/Linear/Linear.sh");
}
