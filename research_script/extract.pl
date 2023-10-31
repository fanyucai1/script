#!/usr/bin/perl -w
use strict;
use warnings;
use Getopt::Long;
use Bio::SeqIO;
my($fasta,$name,$start,$end,$l,$list,$len,$out);
$list||="";
GetOptions(
    "f:s"=>\$fasta,
    "n:s"=>\$name,
    "s:s"=>\$start,
    "e:s"=>\$end,
    "l:s"=>\$l,
    "list:s"=>\$list,
    "o:s"=>\$out,
           );
if(!$fasta)
{
    print "perl $0 -f seq.fa -list list.txt\n";
    print "perl $0 -f seq.fa -n name -l + -o out.fa\n";
    print "perl $0 -f seq.fa -n name -s 1 -e 100 -l +\n";
    print "perl $0 -f seq.fa -n name -s 1 -e 100 -l -\n";
    exit;
}
my %hash2;
if($list ne "")
{
	open(INN,"$list");
	while(<INN>)
	{	
		chomp;
		$hash2{$_}=1;
	}
}
my $in  = Bio::SeqIO->new(-file => $fasta ,-format => 'Fasta');
open(FA,$fasta);
while ( my $seq = $in->next_seq() )
{
    if(exists $hash2{$seq->id})
    {
        print $seq->id,"\n",
    }
}
my %hash;
my $sequence;
while(<FA>)
{
    chomp;
    if($_=~/^\>/)
    {       
        my @array=split(/ /,$_);
        $sequence=substr($array[0],1);
    }
    else
    {
        $hash{$sequence}.=$_;
    }
}
TT:foreach my $key (keys %hash)
{
	if($list ne "")
	{
		if(exists $hash2{$key})
		{
            print ">",$key,"\n",$hash{$key},"\n";
            next TT;
		}
		else
		{
            next TT;
		}
	}   
    if($name eq $key)
    {
        if($end && $start)
        {
            if($l eq "+")
            {
                print ">",$name,"_",$start,"_",$end,"\n",substr($hash{$key},($start-1),($end-$start+1)),"\n";
            }
            else
            {
                my $string=reverse(substr($hash{$key},($start-1),($end-$start+1)));
                $string =~ tr/ACGTacgt/TGCAtgca/;
                print ">",$name,"_",$start,"_",$end,"\n",$string,"\n";
            }
            exit;
        }
        else
        {
            if($l eq "+")
            {
                print ">",$name,"\n",$hash{$key},"\n";
            }
            else
            {
                my $string=reverse $hash{$key};
                $string =~ tr/ACGTacgt/TGCAtgca/;
                print ">",$name,"\n",$string,"\n";
            }
            exit;
        }
    }
}

