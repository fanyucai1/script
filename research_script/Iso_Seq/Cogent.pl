#!/usr/bin/perl -w
use strict;
use warnings;
use Cwd;
use Getopt::Long;
use FindBin qw($Bin);
use Cwd qw(abs_path);
#Before run this script you must import env1,env2 and env3 to your bash_profile.
my $python="/home/fanyucai/software/python/Python-v2.7.9/bin/";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my $env1="export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/home/fanyucai/software/Cogent/Cogent/Complete-Striped-Smith-Waterman-Library/src";
my $env2="export PYTHONPATH=\$PYTHONPATH:/home/fanyucai/software/Cogent/Cogent/Complete-Striped-Smith-Waterman-Library/src";
my $env3="export PATH=\$PATH:/home/fanyucai/software/cDNA_Cupcake/cDNA_Cupcake/sequence:/home/fanyucai/software/minimap/minimap-master/:/home/fanyucai/software/gmap/gmap_v2017.10.30/bin/:/home/fanyucai/software/Mash/mash-Linux64-v2.0/";

my($tran,$outdir,$queue,$prefix,$lines);
$outdir||=getcwd;
$queue||="fat";
GetOptions(
"t:s"=>\$tran,
"o:s"=>\$outdir,
"q:s"=>\$queue,
"p:s"=>\$prefix,
);
sub usage{
    print qq{
Using Cogent to collapse redundant transcripts in absence of genome.

usage:
    perl $0 -t transcript.fasta -o $outdir -q $queue -p prefix
options:
-t      input transcripts
-o      outdir
-q      which queue you will run(default:$queue)

Attention:
Before run this script you must import envriment PATH to your bash_profile as follows::
$env1
$env2
$env3
Email:fanyucai1\@126.com
2017.10.31
    };
    exit;
}
$outdir = abs_path($outdir);
$tran = abs_path($tran);
##################################step1:first Running Family Finding for a large dataset (https://github.com/Magdoll/Cogent/wiki/Running-Cogent)
system "ln -s $tran $outdir/isoseq_flnc.fasta";
system "echo 'cd $outdir/ && $python/python $python/run_preCluster.py --cpus=20'>$outdir/Cogent1.sh";
`perl $qsub --queue $queue --ppn 6 $outdir/Cogent1.sh`;

##################################step2:Run Mash-based family finding on all "bins"
system "mkdir -p $outdir/result/";
system "cd $outdir/ && $python/python $python/generate_batch_cmd_for_Cogent_family_finding.py --cpus=20 --cmd_filename=cmd.sh preCluster.cluster_info.csv preCluster_out result";
`perl $qsub --ppn 5 --lines 3 --maxproc 10 $outdir/cmd.sh`;
#check all script run done whether or not

my @array=glob("$outdir/preCluster_out/*");
while(<1>)
{
    my $i=-1;
    open(FA,">$outdir/check.sh");
    foreach my $key(@array)
    {
        if(! -e "$outdir/preCluster_out/$key/*partition.txt")
        {
            print FA "cd preCluster_out/$key\n";
            print FA "run_mash.py -k 30 --cpus=20 $outdir/preCluster_out/$key/isoseq_flnc.fasta\n";
            print FA "process_kmer_to_graph.py $outdir/preCluster_out/$key/isoseq_flnc.fasta $outdir/preCluster_out/$key/isoseq_flnc.fasta.s1000k30.dist $outdir/result $key\n";
        }
        else
        {
            $i++;
        }
    }
    last if $#array==$i;
    `perl $qsub --ppn 5 --lines 3 --maxproc 10 $outdir/check.sh`;
}
open(OUT,">$outdir/final.partition.txt");
	print OUT "Partition\tSize\tMembers\n";
close OUT;
close FA;
system "cd $outdir && ls preCluster_out/*/*partition.txt | xargs -n1 -i sed \'1d; \$d\' {} | cat >> final.partition.txt";
system "rm -rf $outdir/preCluster_out/ $outdir/preCluster.*";
##################################step3:Coding Genome Reconstruction
system "cd $outdir/ && $python/python $python/generate_batch_cmd_for_Cogent_reconstruction.py --small_genome $outdir/result >$outdir/Coding.sh";
`perl $qsub --ppn 5 --maxproc 10 $outdir/Coding.sh`;
#check all script run done whether or not
@array=glob("$outdir/result/*");
my $kmer=30;
while(<1>)
{
    my $i=-1;
    $kmer+=10;
    open(CH,">$outdir/check");
    foreach my $key(@array)
    {
        if(! -e "$outdir/result/$key/cogent2.fa")
        {
            print CH "cd $outdir/result/$key/ && reconstruct_contig.py --nx_cycle_detection -k $kmer .\n";
        }
        else
        {
            $i++;
        }
    }
    last if $#array==$i;
    `perl $qsub --ppn 5 --maxproc 10 $outdir/check.sh`;
}
##################################step4:Using Cogent to collapse redundant transcripts in absence of genome (https://github.com/Magdoll/Cogent/wiki/Tutorial:-Using-Cogent-to-collapse-redundant-transcripts-in-absence-of-genome)
#Getting the unassigned sequences
open(GMAP,">$outdir/final.sh");
print GMAP "tail -n 1 $outdir/final.partition.txt | tr ',' '\\n' > $outdir/unassigned.list\n";
print GMAP "cd $outdir/ && get_seqs_from_list.py $outdir/all.polished_hq.fasta $outdir/unassigned.list > $outdir/unassigned.fasta\n";
#Concatenate unassigned with Cogent contigs
print GMAP "mkdir $outdir/alignment/ && cd $outdir/alignment/ && cat $outdir/result/*/cogent.fa $outdir/unassigned.fasta > $outdir/alignment/cogent.fake_genome.fasta\n";
#Collapsing redundant isoforms
print GMAP "awk \'{if(\$0~\">\"){++i;print \">Unigene\"i}else{print \$0}}\' $outdir/alignment/cogent.fake_genome.fasta >$outdir/alignment/cogent.fake_genome1.fasta\n";
print GMAP "cd $outdir/alignment/ && gmap_build -D . -d fake_genome $outdir/alignment/cogent.fake_genome1.fasta\n";
print GMAP "cd $outdir/alignment/ && gmap -D . -d fake_genome -f samse -n 0 -t 5 $outdir/all.polished_hq.fasta > $outdir/alignment/isoforms.fasta.sam 2>  $outdir/alignment/isoforms.fasta.sam.log\n";
print GMAP "cd $outdir/alignment/ && sort -k 3,3 -k 4,4n $outdir/alignment/isoforms.fasta.sam > $outdir/alignment/isoforms.fasta.sorted.sam\n";
print GMAP "cd $outdir/alignment/ && $python/python $python/collapse_isoforms_by_sam.py --input $outdir/all.polished_hq.fasta -s $outdir/alignment/isoforms.fasta.sorted.sam -c 0.95 -i 0.85 --dun-merge-5-shorter -o $outdir/alignment/isoforms.fasta.no5merge\n";
print GMAP "cd $outdir/alignment/ && $python/python $python/get_abundance_post_collapse.py $outdir/alignment/isoforms.fasta.no5merge.collapsed $outdir/cluster_report.csv\n";
print GMAP "cd $outdir/alignment/ && $python/python $python/filter_away_subset.py $outdir/alignment/isoforms.fasta.no5merge.collapsed\n";
$lines=`wc -l $outdir/final.sh`;
chomp($lines);
`perl $qsub --queue $queue --lines $lines --ppn 5 $outdir/final.sh`;

