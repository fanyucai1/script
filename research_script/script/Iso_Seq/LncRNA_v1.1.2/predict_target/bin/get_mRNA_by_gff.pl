#!/usr/bin/perl -w
use strict;
use warnings;
use Getopt::Long;
use Data::Dumper;
use FindBin qw($Bin $Script);
use File::Basename qw(basename dirname);
my $BEGIN_TIME=time();
my $version="1.0.0";
#######################################################################################

# ------------------------------------------------------------------
# GetOptions
# ------------------------------------------------------------------
my ($fIn,$gff,$o);
GetOptions(
				"help|?" =>\&USAGE,
				"genome:s"=>\$fIn,
				"gff:s"=>\$gff,
				"o:s"=>\$o,
				) or &USAGE;
&USAGE unless ($fIn and $gff and $o);

my %cds;
my %Strand;
open (IN,$gff) or die $!;
while (<IN>) {
	next unless /\smRNA\s/;
	my ($chr,$type,$start,$end,$strand,$ID)=(split /\s+/,$_)[0,2,3,4,6,8];
	my $geneids=(split/\;|=/,$ID)[1];
	$cds{$chr}{$geneids}{start}=$start;
	$cds{$chr}{$geneids}{end}=$end;
	$Strand{$chr}{$geneids}=$strand;
}
close (IN) ;

$/=">";
open (IN,$fIn) or die $!;
open (OUT,">$o") or die $!;
<IN>;
while (<IN>) {
	chomp;
	next if(/^$/);
	my ($chr,$seq)=split /\n/,$_,2;
		$chr=(split/\s+/,$chr)[0];
		$seq=~s/\s+//ig;
		my $chr_len=length$seq;
		foreach my $geneid (sort keys %{$cds{$chr}}) {
				my $cds=substr($seq,$cds{$chr}{$geneid}{start}-1,$cds{$chr}{$geneid}{end}-$cds{$chr}{$geneid}{start}+1);
				$cds=~tr/atcg/ATCG/;
				if ($Strand{$chr}{$geneid} eq "-") {
					$cds=~tr/ATCG/TAGC/;
					$cds=reverse($cds);
				}
				print OUT ">$geneid $chr $cds{$chr}{$geneid}{start}-$cds{$chr}{$geneid}{end}\n$cds\n";
		}
}
close IN;
close OUT;





#######################################################################################
print STDOUT "\nDone. Total elapsed time : ",time()-$BEGIN_TIME,"s\n";
#######################################################################################

# ------------------------------------------------------------------
# sub function
# ------------------------------------------------------------------
################################################################################################################

sub ABSOLUTE_DIR{ #$pavfile=&ABSOLUTE_DIR($pavfile);
	my $cur_dir=`pwd`;chomp($cur_dir);
	my ($in)=@_;
	my $return="";
	if(-f $in){
		my $dir=dirname($in);
		my $file=basename($in);
		chdir $dir;$dir=`pwd`;chomp $dir;
		$return="$dir/$file";
	}elsif(-d $in){
		chdir $in;$return=`pwd`;chomp $return;
	}else{
		warn "Warning just for file and dir\n";
		exit;
	}
	chdir $cur_dir;
	return $return;
}

################################################################################################################

sub max{#&max(lists or arry);
	#求列表中的最大值
	my $max=shift;
	my $temp;
	while (@_) {
		$temp=shift;
		$max=$max>$temp?$max:$temp;
	}
	return $max;
}

################################################################################################################

sub min{#&min(lists or arry);
	#求列表中的最小值
	my $min=shift;
	my $temp;
	while (@_) {
		$temp=shift;
		$min=$min<$temp?$min:$temp;
	}
	return $min;
}

################################################################################################################

sub revcom(){#&revcom($ref_seq);
	#获取字符串序列的反向互补序列，以字符串形式返回。ATTCCC->GGGAAT
	my $seq=shift;
	$seq=~tr/ATCGatcg/TAGCtagc/;
	$seq=reverse $seq;
	return uc $seq;			  
}

################################################################################################################

sub GetTime {
	my ($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst)=localtime(time());
	return sprintf("%4d-%02d-%02d %02d:%02d:%02d", $year+1900, $mon+1, $day, $hour, $min, $sec);
}


sub USAGE {#
	my $usage=<<"USAGE";
ProgramName:
Version:	$version
Contact:	Zhang XueChuan <zhangxc\@biomarker.com.cn> 
Program Date:   2012.8.23
Usage:
  Options:
  -genome   <file>  genome file,fasta format,forced 
  
  -gff      <file>  gff file,forced 
  
  -o        <file>  output file,fasta format,forced 
  
  -h         Help

USAGE
	print $usage;
	exit;
}
