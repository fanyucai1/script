#!/usr/bin/perl -w
use Getopt::Long;
use strict;
use FindBin qw($Bin);

my $help;
my $input;
my $outdir;
my $db ||='K';
my $sample;
my $species ||= "ko";
my $e_value = 1e-5;
my $method_for_identify ||= "h";
my $false_discovery_rate ||= "BH";
my $number_of_processors ||= 2;
my $standard = "not standard";
my $sp_data_dir = "/allwegene/dat2/software/kobas2.0-20150126/seq_pep/";
my $BlastResult;
my $dirAnnotateResult;
my $dirIndentifyResult;
my $dirAnnotate = "/allwegene/dat2/software/kobas2.0-20150126/scripts/annotate.py";
my $dirIdentify = "/allwegene/dat2/software/kobas2.0-20150126/scripts/identify.py";
GetOptions("h|help" => \$help,
           "i=s" => \$input,
           "o=s" => \$outdir,
           "s=s" => \$species,
           "sn=s" => \$sample,
           "e=f" => \$e_value,
           "m=s" => \$method_for_identify,
           "f=s" => \$false_discovery_rate,
           "n=i" => \$number_of_processors,
           "d=s"=> \$db,
           "blast-result=s" => \$BlastResult,
           ) or die "Cannot get the inputs: $!";

my $sp_name_list;
my $sp_name_data;

if (!defined($outdir) || !defined($input) || defined($help))
{
	&usage;
	exit 0;
}

if(!-d $outdir){`mkdir -p $outdir`;}
my $dirTemp;
$dirTemp = "$outdir/temp";
$dirTemp =~ s/\/\//\//;
unless (-d $dirTemp)
{
        !system "mkdir -p $dirTemp" or warn "Something went wrong!";
}

opendir SP_DATA, $sp_data_dir or die "Cannot open the folder: $!";
foreach my $file (readdir SP_DATA)
{
  if ($file =~ /^($species).+?fasta$/)
  {
    $sp_name_data = $file;
    last;
  }
}
closedir SP_DATA;

$sp_data_dir = "$sp_data_dir\/$sp_name_data";
#print "$sp_data_dir\n";

my $dirBlastResult = "$dirTemp/$sample.blast";
$dirAnnotateResult = "$dirTemp/$sample.annotate";
$dirIndentifyResult = "$outdir/$sample.identify.xls";
$dirIndentifyResult =~ s/\/\//\//;

open SH,">$outdir/$sample.run_kobas.sh";
print SH "echo \"================ 1.blast =================\"\n";
print SH "python $Bin/scripts/KEGG_step1_blast.py $input  $species $dirBlastResult $dirTemp/$sample.blast.sh\n\n";
print SH "sh $dirTemp/$sample.blast.sh\n\n";
print SH "export LD\_LIBRARY\_PATH\=\$LD\_LIBRARY\_PATH\:\/allwegene\/dat2\/software\/R-3.2.2\/lib64\/R\/lib\nPATH\=\/allwegene\/dat2\/software\/Python-2.7\/bin\:\$PATH\:\$HOME\/bin\nexport PATH\n";
print SH "echo \"================ 2.annotate =================\"\n";
if ($species eq "000" || $species eq "001" || $species eq "002")
{
	print SH "/allwegene/dat2/software/Python-2.7/bin/python $dirAnnotate -i $dirBlastResult -t blastout:tab -s ko -n $number_of_processors -e $e_value -o $dirAnnotateResult\n";
}
else
{
	print SH "/allwegene/dat2/software/Python-2.7/bin/python $dirAnnotate -i $dirBlastResult -t blastout:tab -s $species -n $number_of_processors -e $e_value -o $dirAnnotateResult\n";
}

## for identify
print SH "echo \"================ 3.identify =================\"\n";
if ($species eq "000" || $species eq "001" || $species eq "002")
{
	print SH "/allwegene/dat2/software/Python-2.7/bin/python $dirIdentify -f $dirAnnotateResult -d $db -m $method_for_identify -n $false_discovery_rate -b ko -s $standard -o $dirIndentifyResult\n";
}
else
{
	print SH "/allwegene/dat2/software/Python-2.7/bin/python $dirIdentify -f $dirAnnotateResult -d $db -m $method_for_identify -n $false_discovery_rate -b $species -o $dirIndentifyResult\n";
}
print SH "echo \"=============== extract top20 significant pathways  ================\"\n";
print SH "perl $Bin/scripts/merge_annotate_identify_files.pl $dirAnnotateResult $dirIndentifyResult $outdir/add.$sample.identify.xls\n";
print SH "perl $Bin/scripts/extract_top20.pl $outdir/add.$sample.identify.xls >$outdir/top20.$sample.identify.xls\n";
print SH "sed -i \"s\/'\/ \/g\" $outdir/top20.$sample.identify.xls\n";
print SH "/allwegene/dat2/software/R-3.2.2/bin/Rscript $Bin/scripts/Pathwayscatter.R $sample $outdir $outdir/top20.$sample.identify.xls\n";
print SH "mv $outdir/add.$sample.identify.xls $outdir/$sample.KEGG_pathway_enrichment_result.xls\n";
close SH;
#------------------------------------------------

sub usage
{
	print STDERR <<USAGE;
===============================================================================
kobas2.0
Function: KOBAS 2.0 is an update of KOBAS (KEGG Orthology Based Annotation System). Its purpose is to identify statistically enriched related pathways and diseases for a set of genes or proteins, using pathway and disease knowledge from
multiple commonly used databases.
-------------------------------------------------
Description:  This script is used to generate run KOBAS shell scripts
Usage: runKOBAS.pl [options]
options:
	-i	<string>	input diffgene.id.fa files. <Required>
	-o	<string>	output directory.  <Required>
	-s	<string>	abbr for species, default: ko (KEGG Orthology)
	-sn	<string>	prefix of name you analyze,eg: KOvsWX_ALL
	-e	<float>		e value, default:1e-5
	-m	<string>	statistic method for identify, b is binomial
				test, c is chisquare test, f is fisher exact
				test, h is hypergeometric test and x is
				frequency list. Default: hypergeometric test.
	-f	<string>	false discovery rate correction method: QVALUE,
				BH, BY or none. Default: QVALUE.
	-n	<int>		number of processors, default: 2
	-d     <string>         databases for selection, 1-letter abbreviation
                        	separated by "/": K for KEGG PATHWAY, n for PID, b for
                        	BioCarta, R for Reactome, B for BioCyc, p for PANTHER,
                        	o for OMIM, k for KEGG DISEASE, f for FunDO, g for
                        	GAD, N for NHGRI GWAS Catalog and G for Gene Ontology,
                        	eg: K/n/b/R/B/p/o/k/f/g/N/G, default: K
-------------------------------------------------
USAGE
}
