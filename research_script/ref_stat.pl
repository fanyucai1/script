#!/usr/bin/perl -w
use	strict;
use warnings;
use	Getopt::Long;
use	Data::Dumper;
use Cwd qw(abs_path getcwd);
use FindBin qw($Bin $Script);
use File::Basename qw(basename dirname);
my $program_name=basename($0);
use List::Util qw/max min sum/;
use Bio::SeqIO;
use POSIX;
my $ver="1.0";
############################################
my %opts;
GetOptions(\%opts,"ref=s","od=s","h");
if (!defined($opts{ref})||defined($opts{h})) {
	&help();
}
sub help{
	print << "	Usage End.";
	Description:
		Count fasta  length and GC percent.
	version:$ver
	Usage:
		
		-ref     reference fasta file     must be given;
		-od      outdir                   default cwd;

	Usage End.
		exit;
}
###############Time
my $BEGIN=time();
my $Time_Start;
$Time_Start = sub_format_datetime(localtime(time()));
print "\nStart $program_name Time :[$Time_Start]\n\n";
###############
my $ref=abs_path($opts{ref});
$opts{od}||=getcwd;
my $outdir=abs_path($opts{od});
mkdir "$outdir" if(!-d $outdir);
my $outkey=basename($ref);
my$in  = Bio::SeqIO->new(-file => "$ref" ,
                               -format => 'Fasta');
                               
open L,">$outdir/$outkey.stat"||die;

my @Total_len=();my $Total_N=0;my @Total_GC=();
my$N50_length;my$N90_length;my$seq_num=0;

my @Total_len_scaffold=();my $Total_N_scaffold=0;my @Total_GC_scaffold=();
my$N50_length_scaffold;my$N90_length_scaffold;my$seq_num_scaffold=0;

my @Total_len_chr=();my $Total_N_chr=0;my @Total_GC_chr=();
my$N50_length_chr;my$N90_length_chr;my$seq_num_chr=0;


while ( my $sequence = $in->next_seq() ) {

	$seq_num++;
	my ($chr,$seq,$desc)=($sequence->id,$sequence->seq,$sequence->desc);
	my$l=$sequence->length;
	my$n= () =$seq =~ /N/gi;
	$Total_N=$Total_N+$n;
	my$gc=() =$seq =~ /[GC]/gi;
	$gc=$gc/($l-$n);
	
	if( $chr=~/chr/i || $desc=~/chromosome/i ){
		$seq_num_chr++;
		push @Total_len_chr,$l;
		push @Total_GC_chr,$gc;
		$Total_N_chr=$Total_N_chr+$n;
	}
	if($chr=~/scaffold/i|| $desc=~/scaffold/i){
		$seq_num_scaffold++;
		push @Total_len_scaffold,$l;
		push @Total_GC_scaffold,$gc;
		$Total_N_scaffold=$Total_N_scaffold+$n;
	}
	
	push @Total_len,$l;
	push @Total_GC,$gc;
     print "$chr\t$l\n";

}
$in->close();
if($seq_num_chr and $seq_num_scaffold){
	

	print L "Seq_type\tSeq_number\tTotal_length\tGC_content(%)\tN_content(%)\tN50_length\tN90_length\n";
	
		print L "Chromosome\t$seq_num_chr\t";
	my$Total_length_chr=sum(@Total_len_chr);
	$Total_length_chr=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
	print L "$Total_length_chr\t";
	my$GC_content_chr=sum(@Total_GC_chr)/$seq_num_chr;
	printf L "%2.2f%%\t",$GC_content_chr*100;
	my$N_content_chr=$Total_N_chr/sum(@Total_len_chr);
	printf L "%2.2f%%\t",$N_content_chr*100;
	
	@Total_len_chr=reverse sort {$a<=>$b}@Total_len_chr;
	if($seq_num_chr ==1){
		my$N50_chr= $Total_len_chr[0];
		$N50_chr=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N50_chr\t"; 
		my$N90_chr= $Total_len_chr[0];
		$N90_chr=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N90_chr\n"; 
	}else{
		my$N50_chr= $Total_len_chr[POSIX::floor($seq_num_chr*0.5)];
		$N50_chr=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N50_chr\t"; 
		my$N90_chr= $Total_len_chr[POSIX::floor($seq_num_chr*0.9)];
		$N90_chr=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N90_chr\n"; 
	
	}
	
		print L "Scaffold\t$seq_num_scaffold\t";
	my$Total_length_scaffold=sum(@Total_len_scaffold);
	$Total_length_scaffold=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
	print L "$Total_length_scaffold\t";
	my$GC_content_scaffold=sum(@Total_GC_scaffold)/$seq_num_scaffold;
	printf L "%2.2f%%\t",$GC_content_scaffold*100;
	my$N_content_scaffold=$Total_N_scaffold/sum(@Total_len_scaffold);
	printf L "%2.2f%%\t",$N_content_scaffold*100;
	
	@Total_len_scaffold=reverse sort {$a<=>$b}@Total_len_scaffold;
	if($seq_num_scaffold ==1){
		my$N50_scaffold= $Total_len_scaffold[0];
		$N50_scaffold=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N50_scaffold\t"; 
		my$N90_scaffold= $Total_len_scaffold[0];
		$N90_scaffold=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N90_scaffold\n"; 
	}else{
		my$N50_scaffold= $Total_len_scaffold[POSIX::floor($seq_num_scaffold*0.5)];
		$N50_scaffold=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N50_scaffold\t"; 
		my$N90_scaffold= $Total_len_scaffold[POSIX::floor($seq_num_scaffold*0.9)];
		$N90_scaffold=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N90_scaffold\n"; 
	
	}

	print L "Chromosome+Scaffold\t$seq_num\t";
	my$Total_length=sum(@Total_len);
	$Total_length=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
	print L "$Total_length\t";
	my$GC_content=sum(@Total_GC)/$seq_num;
	printf L "%2.2f%%\t",$GC_content*100;
	my$N_content=$Total_N/sum(@Total_len);
	printf L "%2.2f%%\t",$N_content*100;
	
	@Total_len=reverse sort {$a<=>$b}@Total_len;
	if($seq_num ==1){
		my$N50= $Total_len[0];
		$N50=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N50\t"; 
		my$N90= $Total_len[0];
		$N90=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N90\n"; 
	}else{
		my$N50= $Total_len[POSIX::floor($seq_num*0.5)];
		$N50=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N50\t"; 
		my$N90= $Total_len[POSIX::floor($seq_num*0.9)];
		$N90=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N90\n"; 
	
	}
	
	close(L);

}else{
	print L "Seq_number\tTotal_length\tGC_content(%)\tN_content(%)\tN50_length\tN90_length\n";
	print L "$seq_num\t";
	my$Total_length=sum(@Total_len);
	$Total_length=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
	print L "$Total_length\t";
	my$GC_content=sum(@Total_GC)/$seq_num;
	printf L "%2.2f%%\t",$GC_content*100;
	my$N_content=$Total_N/sum(@Total_len);
	printf L "%2.2f%%\t",$N_content*100;
	
	@Total_len=reverse sort {$a<=>$b}@Total_len;
	if($seq_num ==1){
		my$N50= $Total_len[0];
		$N50=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N50\t"; 
		my$N90= $Total_len[0];
		$N90=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N90\n"; 
	}else{
		my$N50= $Total_len[POSIX::floor($seq_num*0.5)];
		$N50=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N50\t"; 
		my$N90= $Total_len[POSIX::floor($seq_num*0.9)];
		$N90=~s/(?<=\d)(?=(\d\d\d)+$)/,/g;
		print L "$N90\n"; 
	
	}
	
	close(L);
}
################Time
my $Time_End;
$Time_End = sub_format_datetime(localtime(time()));
&Runtime($BEGIN);
print "\nEnd $program_name Time :[$Time_End]\n\n";
###############Subs
sub calcGC {
 my $seq = $_[0];
 my $len = $_[1];
 my $count = 0;
 $count++ while ($seq =~ m/[GC]/gi);
 my $num = $count / $len;
 #my ($dec) = $num =~ /(\S{0,6})/;
 return $num;
}
sub calcN {
 my $seq = $_[0];
 my $count = 0;
 $count++ while ($seq =~ m/[N]/gi);
 #my $num = $count / length($seq);;
 #my ($dec) = $num =~ /(\S{0,6})/;
 return $count;
}

sub sub_format_datetime {#Time calculation subroutine
	my($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = @_;
	$wday = $yday = $isdst = 0;
	sprintf("%4d-%02d-%02d %02d:%02d:%02d", $year+1900, $mon+1, $day, $hour, $min, $sec);
}
sub Runtime{ # &Runtime($BEGIN);
	my ($t1)=@_;
	my $t=time()-$t1;
	print "\nTotal elapsed time: ${t}s\n";
}

