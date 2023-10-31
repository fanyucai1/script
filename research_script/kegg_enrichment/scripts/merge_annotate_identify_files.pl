#!/usr/bin/perl
die "perl $0 <ko annotation from annotate.py> <enrichment result from identify.py>  <merged.outputfile>\n" unless @ARGV==3;
my $annot_result=shift;
my $identify_result=shift;
my $outfile=shift;

my %ko;
my %Entrez;
## begin to read annotate file
open AN, $annot_result or die "cannot open $annot_result !";
while (<AN>) {
	chomp;
	if (/\/\/\/\//) {
		last;
	}
	if (/^\w/) {
		my @tmp=split /\t/;
		my @IDs=split /\|/,$tmp[1];
		if ($IDs[0] eq "None") {
			$ko{$tmp[0]}=" ";
			$Entrez{$tmp[0]}=" ";
		}
		else
		{
			$ko{$tmp[0]}=$IDs[0];
			$Entrez{$tmp[0]}=" ";
		}
	}
}

$/="\/\/\/\/\n";
while (<AN>) {
	chomp;
	my $line=$_;
	my @tmp=split /\n/,$line;
	my @tmp1=split /\s+/,$tmp[0];
	if($tmp1[0]=~/Query:/){
		if($line=~/Entrez Gene ID:\s+(?<entrez>\d+)/){
			$Entrez{$tmp1[1]}=$+{entrez};
		}
	}
	else
		{next;}
}
close AN;

$/="\n";

open OUT ,">$outfile" or die "$!\n";
open PA, $identify_result or die "cannot open $identify_result !";
while (<PA>) {
	chomp;
	if(/^##/||/^kobas/||/^\/allwegene/){next;}
	elsif (/^\#Term/) {
		my @tmp=split /\t/;
		print OUT  "$tmp[0]\t$tmp[1]\t$tmp[2]\t$tmp[3]\t$tmp[4]\t$tmp[5]\t$tmp[6]\t$tmp[7]\tKEGG_ID/KO\tEntrez_ID\t$tmp[8]\n";
	}elsif (/^[\w@]/) {
		my @tmp=split /\t/;
		my @id=split/\|/,$tmp[7];
		my $ko_id="";
		my $Entrez_id="";
		foreach my $i (@id) {
			$ko_id .=$ko{$i}."\|";
			$Entrez_id .=$Entrez{$i}."\|";
		}
		print OUT  "$tmp[0]\t$tmp[1]\t$tmp[2]\t$tmp[3]\t$tmp[4]\t$tmp[5]\t$tmp[6]\t$tmp[7]\t$ko_id\t$Entrez_id\t$tmp[8]\n";
	}
	else
	{
		print OUT "$_\n";
	}
}
close PA;
close OUT;
