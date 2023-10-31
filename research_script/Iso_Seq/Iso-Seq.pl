#!/usr/bin/perl -w
#https://github.com/PacificBiosciences/IsoSeq_SA3nUP/wiki
use strict;
use warnings;
use Cwd;
use Getopt::Long;
use FindBin qw($Bin);
my ($bam,$outdir,$minlen,$maxlen,$par,$ignore_polyA,$cluster,$minpass);
my $smrtlink="/opt/smrtlinks/";
my $qsub="/home/fanyucai/software/qsub/qsub-pbs.pl";
my $python13="/home/fanyucai/software/python/Python-v2.7.13/bin";
my $gmap="/home/fanyucai/software/gmap/gmap-v2017.03.17/bin";
my $lncrnas="/home/fanyucai/software/LncRNAs_pipeline/lncrnas-pipeline";
my $PLEK="/home/fanyucai/software/PLEK/PLEK.1.2/";
my $Blasr="/opt/smrtlinks/install/smrtlink-fromsrc_4.0.0.190159+190159-190159-189856-189856-189856/bundles/smrttools/install/smrttools-fromsrc_4.0.0.190159/private/pacbio/blasr/bin/";

$minlen||=300;
$maxlen||=15000;
$minpass||=2;
GetOptions(
    "bam:s"=>\$bam,
    "o:s"=>\$outdir,
    "minlen:s"=>\$minlen,
    "ignore_polyA:s"=>\$ignore_polyA,
           );

sub usage{
    print qq{
 This script will run the Iso-seq pipeline.
 usage:
1:perl $0 -bam subreads.bam -o /path/to/outputdirectory/ -ignore_polyA true
            or
2:perl $0 -bam lib1.subreads.bam,lib2.subreads.bam,lib3.subreads.bam -o /path/to/outputdirectory/ -ignore_polyA false
 
 options:
 -bam               the bam file(force)
 -o                 output directory
 -cpu               cpu number(default:20)
 -minlen            min_sequence_length
 -maxlen            max_sequence_length
 -ignore_polyA      whether no polyA tail in your transcripts:true or false(force)
 -cluster           PacBio
 
 Email:fanyucai1\@126.com
 2017.4.13
    };
exit;
}
sub qsub()
{
    my ($shfile, $queue, $ass_maxproc,$resource) = @_ ;
    $queue||="Pacbio";
    $ass_maxproc||=15;
    $resource||="mem=20G";
    my $cmd = "perl $qsub --maxproc $ass_maxproc --queue $queue --resource $resource --reqsub $shfile" ;
    my $flag=system($cmd);
    if($flag !=0)
    {
        die "qsub [$shfile] die with error : $cmd \n";
        exit;
	}
}
if(!$ignore_polyA ||!$bam ||!$outdir)
{
    &usage();
}
###################################prepare
open(ISO,">$outdir/Iso_seq.sh");
my @merge=split(/\,/,$bam);
if($#merge>0)
{
    my $tmp;
    foreach my $key(@merge)
    {
        $tmp.="$key ";
    }
    print ISO "cd $outdir/ && $smrtlink/smrtcmds/bin/dataset create --type SubreadSet output.ccs.xml $tmp\n";
}
else
{
    print ISO "cd $outdir/ && $smrtlink/smrtcmds/bin/dataset create --type SubreadSet output.ccs.xml $bam\n";
}
&qsub("$outdir/Iso_seq.sh");

#####################################run the Iso-seq
system "cd $outdir/ && $smrtlink/smrtcmds/bin/pbsmrtpipe show-template-details pbsmrtpipe.pipelines.sa3_ds_isoseq -o isoseq.xml";
system "cp $smrtlink/userdata/config/preset.xml $outdir/global.xml";
system "mkdir -p $outdir/tmp_dir/";
`sed -i "41c <value>$outdir/tmp_dir</value>" $outdir/global.xml`;
`sed -i "29c <value>$minlen</value>" $outdir/isoseq.xml`;
`sed -i "71c <value>$maxlen</value>" $outdir/isoseq.xml`;
`sed -i "41c <value>$minpass</value>" $outdir/isoseq.xml`;
if($ignore_polyA =~/t/i)
{
    `sed -i "32c <value>True</value>" $outdir/isoseq.xml`;
}

system  "echo 'cd $outdir/ && $smrtlink/smrtcmds/bin/pbsmrtpipe pipeline-id pbsmrtpipe.pipelines.sa3_ds_isoseq -e eid_subread:output.ccs.xml --preset-xml=isoseq.xml --preset-xml=global.xml --output-dir=Iso_Seq'>$outdir/step1.sh\n";
system "nohup sh $outdir/step1.sh&";


