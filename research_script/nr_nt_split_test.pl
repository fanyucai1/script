#!/usr/bin/perl -w
use strict;
use warnings;
use Cwd;
use FindBin qw($Bin);
use Getopt::Long;
use Cwd;
my $outdir;
$outdir||=getcwd;
my $node=shift;#nodes.dump. from ncbi
my $gi=shift;# the first (left) column is the GenBank identifier (gi) of nucleotide record, the second (right) column is  taxonomy identifier (taxid). from ncbi
my $type=shift;#nucl or prot
my $db=shift;#index file  of nr or nr from ncbi
my $blastdb_aliastool="/home/fanyucai/software/blast+/ncbi-blast-2.6.0+/bin/blastdb_aliastool";
my $blastdbcmd="/home/fanyucai/software/blast+/ncbi-blast-2.6.0+/bin/blastdbcmd";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
sub qsub()
{
	my ($shfile, $queue, $ass_maxproc) = @_ ;
    $queue||="all";
    $ass_maxproc||=10;
    my $cmd = "perl $qsub --maxproc $ass_maxproc --queue $queue --reqsub $shfile --independent" ;
    my $flag=system($cmd);
    if($flag !=0)
    {
		die "qsub [$shfile] die with error : $cmd \n";
        exit;
	}
}
if(!$node || !$gi || !$type|| !$db)
{
    print "perl $0 nodes.dmp gi_taxid_nucl.dmp nucl  nt\n";
    print "perl $0 nodes.dmp gi_taxid_prot.dmp pro   nr\n";
    print "fanyucai1\@126.com\n";
    exit;
}
=head
system "sed -e \'s/\t//g\' $node >$outdir/new_nodes.dmp";
open(NODE,"$outdir/new_nodes.dmp");
my %tax;
while(<NODE>)
{
    chomp;
    my @array=split(/\|/,$_);
    $tax{$array[0]}=$array[4];#tax_id--->division id
}
open(GI,$gi);
open(BCT,">$outdir/BCT.list");
open(INV,">$outdir/INV.list");
open(MAM,">$outdir/MAM.list");
open(PHG,">$outdir/PHG.list");
open(PLN,">$outdir/PLN.list");
open(PRI,">$outdir/PRI.list");
open(ROD,">$outdir/ROD.list");
open(SYN,">$outdir/SYN.list");
open(UNA,">$outdir/UNA.list");
open(VRL,">$outdir/VRL.list");
open(VRT,">$outdir/VRT.list");
open(ENV,">$outdir/ENV.list");
open(OTH,">$outdir/OTH.list");

my $num=0;
TT:while(<GI>)
{
    $num++;
    chomp;
    my @array=split(/\t/,$_);
if(exists $tax{$array[1]})
{
    if($tax{$array[1]} == "0")
    {
        print BCT "$array[0]\n";
        next TT;
    }
    if( $tax{$array[1]} == "1")
    {
        print INV "$array[0]\n";
        next TT;
    }
    if( $tax{$array[1]} == "2")
    {
        print MAM "$array[0]\n";
        next TT;
    }
    if( $tax{$array[1]} == "3")
    {
        print PHG "$array[0]\n";
        next TT;
    }
    if( $tax{$array[1]} == "4")
    {
        print PLN "$array[0]\n";
        next TT;
    }
    if( $tax{$array[1]} == "5")
    {
        print PRI "$array[0]\n";
        next TT;
    }
    if( $tax{$array[1]} == "6")
    {
        print ROD "$array[0]\n";
        next TT;
    }
    if( $tax{$array[1]} == "7")
    {
        print SYN "$array[0]\n";
        next TT;
    }
    if($tax{$array[1]} == "8")
    {
        print UNA "$array[0]\n";
        next TT;
    }
    if($tax{$array[1]} == "9")
    {
        print VRL "$array[0]\n";
        next TT;
    }
    if( $tax{$array[1]} == "10")
    {
        print VRT "$array[0]\n";
        next TT;
    }
    if($tax{$array[1]} == "11")
    {
        print ENV "$array[0]\n";
        next TT;
    }
}
else
{
        print OTH "$array[0]\n";
        next TT;
}
}
=cut
open(FA,">$outdir/index.sh");
print FA "$blastdb_aliastool -db $db -dbtype $type -gilist $outdir/BCT.list -out $outdir/nr_BCT\n";
print FA "$blastdb_aliastool -db $db -dbtype $type -gilist $outdir/INV.list -out $outdir/nr_INV\n";
print FA "$blastdb_aliastool -db $db -dbtype $type -gilist $outdir/MAM.list -out $outdir/nr_MAM\n";
print FA "$blastdb_aliastool -db $db -dbtype $type -gilist $outdir/PHG.list -out $outdir/nr_PHG\n";
print FA "$blastdb_aliastool -db $db -dbtype $type -gilist $outdir/PLN.list -out $outdir/nr_PLN\n";
print FA "$blastdb_aliastool -db $db -dbtype $type -gilist $outdir/PRI.list -out $outdir/nr_PRI\n";
print FA "$blastdb_aliastool -db $db -dbtype $type -gilist $outdir/ROD.list -out $outdir/nr_ROD\n";
print FA "$blastdb_aliastool -db $db -dbtype $type -gilist $outdir/SYN.list -out $outdir/nr_SYN\n";
print FA "$blastdb_aliastool -db $db -dbtype $type -gilist $outdir/UNA.list -out $outdir/nr_UNA\n";
print FA "$blastdb_aliastool -db $db -dbtype $type -gilist $outdir/VRL.list -out $outdir/nr_VRL\n";
print FA "$blastdb_aliastool -db $db -dbtype $type -gilist $outdir/VRT.list -out $outdir/nr_VRT\n";
print FA "$blastdb_aliastool -db $db -dbtype $type -gilist $outdir/ENV.list -out $outdir/nr_ENV\n";

&qsub("$outdir/index.sh");

=head
open(FA2,">$outdir/extract.sh");
print FA2 "$blastdbcmd -db $db -dbtype \'prot\' -entry_batch $outdir/BCT.list -out $outdir/nr_BCT\n";
print FA2 "$blastdbcmd -db $db -dbtype \'prot\' -entry_batch $outdir/INV.list -out $outdir/nr_INV\n";
print FA2 "$blastdbcmd -db $db -dbtype \'prot\' -entry_batch $outdir/MAM.list -out $outdir/nr_MAM\n";
print FA2 "$blastdbcmd -db $db -dbtype \'prot\' -entry_batch $outdir/PHG.list -out $outdir/nr_PHG\n";
print FA2 "$blastdbcmd -db $db -dbtype \'prot\' -entry_batch $outdir/PLN.list -out $outdir/nr_PLN\n";
print FA2 "$blastdbcmd -db $db -dbtype \'prot\' -entry_batch $outdir/PRI.list -out $outdir/nr_PRI\n";
print FA2 "$blastdbcmd -db $db -dbtype \'prot\' -entry_batch $outdir/ROD.list -out $outdir/nr_ROD\n";
print FA2 "$blastdbcmd -db $db -dbtype \'prot\' -entry_batch $outdir/SYN.list -out $outdir/nr_SYN\n";
print FA2 "$blastdbcmd -db $db -dbtype \'prot\' -entry_batch $outdir/UNA.list -out $outdir/nr_UNA\n";
print FA2 "$blastdbcmd -db $db -dbtype \'prot\' -entry_batch $outdir/VRL.list -out $outdir/nr_VRL\n";
print FA2 "$blastdbcmd -db $db -dbtype \'prot\' -entry_batch $outdir/VRT.list -out $outdir/nr_VRT\n";
print FA2 "$blastdbcmd -db $db -dbtype \'prot\' -entry_batch $outdir/ENV.list -out $outdir/nr_ENV\n";
`perl $qsub $outdir/extract.sh`;
=cut