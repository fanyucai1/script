#!/usr/bin/env perl
use warnings;
use strict;
use File::Spec;
use FindBin qw($Bin);
use File::Basename;
use Getopt::Long;
use IO::File;
use XML::Writer;
use Config::IniFiles;

######################################### software ########################################
my $xml2html="/home/fanyucai/script/xml2html/xml2HtmlConverter.py";
my $python="/home/fanyucai/software/python/Python-v2.7.13/bin/python";
###########################################################################################

my ($idir, $odir, $config, $help);
GetOptions(
        "i:s"       =>\$idir,
        "o:s"       =>\$odir,
        "c:s"       =>\$config,
        "help|h!"   =>\$help,
);

my $usage =<<"USAGE";
Program: $0
Options:
        -i       <indir>   input analysis dir                            [Required]
        -c       <file>    config file                                   [Required]
        -o       <outdir>  output dir                                    [Required]
        -help|h            print help information
Example:
	perl rna_vs_rna_report.pl -i OEXX -c config.ini -o OEXX_report_20180121

USAGE

die $usage if(!$idir || !$odir || !$config || $help);
(-d $idir) || die "Error: don't find indir: $idir!\n";
$idir = File::Spec->rel2abs($idir);$idir=~s/\/$//g;
(-d $odir) && system("rm -r $odir"); mkdir $odir;
$odir = File::Spec->rel2abs($odir);$odir=~s/\/$//g;
(-s $config) || die "Error: don't find config file: $config!\n";
$config = File::Spec->rel2abs($config);

### 拷贝结果
my $result="$odir/result";
mkdir $result;

my %ini;
tie %ini, 'Config::IniFiles', (-file =>$config);
$ini{RNA_vs_RNA}{header}=File::Spec->rel2abs($ini{RNA_vs_RNA}{header});

my @group=split /,/,$ini{RNA_vs_RNA}{group};
open CP,">$odir/copy.sh" || die $!;
for my $g(@group){
	print CP "cp $idir/{$g.$ini{RNA_vs_RNA}{name1}\_$ini{RNA_vs_RNA}{name2}.xls,$g.$ini{RNA_vs_RNA}{name1}\_$ini{RNA_vs_RNA}{name2}.pdf,$g.$ini{RNA_vs_RNA}{name1}\_$ini{RNA_vs_RNA}{name2}.png} $result\n";
	print CP "cp $idir/{$g.$ini{RNA_vs_RNA}{name1}\_$ini{RNA_vs_RNA}{name2}.edges.xls,$g.$ini{RNA_vs_RNA}{name1}\_$ini{RNA_vs_RNA}{name2}.nodes.xls} $result\n";
}
close CP;
system("sh $odir/copy.sh && rm $odir/copy.sh");

mkdir "$odir/pic";
system("cp $Bin/pic/* $odir/pic");
system("cp $ini{RNA_vs_RNA}{header} $odir/pic");
#客户信息表格写入
open(Project, ">$odir/pic/Project.txt") or die $!;
print Project "合同编号\t$ini{main_par}{compact_NUM}\n";
print Project "客户姓名\t$ini{main_par}{customer}\n";
print Project "实验物种\t$ini{main_par}{specie}\n";
print Project "执行编码\t$ini{main_par}{exc_num}\n";
close(Project);

my $output = IO::File->new(">$odir/output.xml");
my $writer = XML::Writer->new(OUTPUT => $output,NAMESPACES => 1);
$writer->xmlDecl("UTF-8");
my $pic; my $tab;
#first report title
print $output "\n";$writer->startTag("report");
print $output "\n";$writer->emptyTag("report_name", "value" => $ini{main_par}{title});
#abstract
print $output "\n";$writer->emptyTag("report_abstract", "value"=>"");
#客户信息表格
print $output "\n";$writer->emptyTag('h1', 'name'=>"项目信息",'type'=>"一级标题显示样式",'desc'=>"一级标题描述");
print $output "\n";$writer->emptyTag('table','name'=>"",'type'=>"type1|full",'desc'=>"",'path'=>"pic/Project.txt");
print $output "\n";$writer->emptyTag('h1', 'name'=>"分析流程",'type'=>"一级标题显示样式",'desc'=>"一级标题描述");
print $output "\n";$writer->emptyTag('p','type'=>'正文段落显示样式','desc'=>"mircroRNA负调控流程图如下：");
print $output "\n";$writer->emptyTag('pic', 'name'=>"图".++$pic." mircroRNA负调控流程图",'desc'=>"",'path'=>"pic/pip.png");
print $output "\n";$writer->emptyTag('h1', 'name'=>"分析结果",'type'=>"一级标题显示样式",'desc'=>"一级标题描述");

print $output "\n";$writer->emptyTag('p','type'=>'正文段落显示样式','desc'=>"miRNA是一类进化上保守的非编码小分子RNA，具有在翻译水平调控基因表达的功能。主要通过作用于多个靶基因在很多信号通路，如发育、分化、增殖、细胞凋亡中发挥重要作用。miRNA可以结合mRNA，使之降解或者抑制其翻译表达。近年来的研究也发现，lncRNA，环状RNA在不同物种中起到miRNA海绵的作用，称之为竞争性內源RNA（ceRNA），能竞争性结合miRNA，从而调控靶基因的表达。");
print $output "\n";$writer->emptyTag('p','type'=>'正文段落显示样式','desc'=>"miRNA-转录组负调控关联分析，即根据预测的miRNA与靶标转录本的相互作用关系对列表（miRNA与转录本靶标关系预测：对于动物，使用miranda软件软件来预测，植物则使用psRNATarget软件来预测），miRNA差异筛选结果及特定模块的差异转录本（mRNA/lncRNA/circRNA），获得miRNA与特定转录本间的负调控关系对，并构建microRNA负调控网络图。");
print $output "\n";$writer->emptyTag('p','type'=>'正文段落显示样式','desc'=>$ini{RNA_vs_RNA}{name1}."-".$ini{RNA_vs_RNA}{name2}."负调控网络图如下：");
my @picture=glob "$result/*png";
print $output "\n";$writer->startTag('pic_list','name'=>"图".++$pic." ".$ini{RNA_vs_RNA}{name1}."-".$ini{RNA_vs_RNA}{name2}."负调控网络图",'type'=>'图片列表显示样式','desc'=>"图片说明：".$ini{RNA_vs_RNA}{name1}."是三角形，".$ini{RNA_vs_RNA}{name2}."是圆，红色代表上调，绿色代表下调，图形越大说明与之相连的节点越多。");
for my $p (@picture){
	print $output "\n"; $writer->emptyTag('pic', 'name'=>basename($p), 'desc'=>"",'path'=>"result/".basename($p));
}
print $output "\n";$writer->endTag("pic_list");
print $output "\n";$writer->emptyTag('p','type'=>'正文段落显示样式','desc'=>$ini{RNA_vs_RNA}{name1}."-".$ini{RNA_vs_RNA}{name2}."负调控结果表格说明如下：");
print $output "\n";$writer->emptyTag('table','name'=>"表".++$tab." ".$ini{RNA_vs_RNA}{name1}."-".$ini{RNA_vs_RNA}{name2}."负调控结果表格说明",'type'=>"type1|full",'desc'=>"",'path'=>"pic/".basename($ini{RNA_vs_RNA}{header}));
print $output "\n";$writer->emptyTag('p','type'=>'正文段落显示样式','desc'=>"结果文件：");
my @tablefile=grep {$_!~/edges|nodes/} glob "$result/*xls";
foreach my $f (@tablefile){
	$writer->emptyTag('file','name'=>basename($f),'type'=>"文件显示样式",'desc'=>"",'path'=>"result/".basename($f),'action'=>"文件类型");
}

print $output "\n";$writer->endTag("report");
print $output "\n";$writer->end();
print $output "\n";$output->close();
system("export PATH=/home/fanyucai/software/ImageMagick/ImageMagick-v6.8.9-10/bin/:\$PATH && export LD_LIBRARY_PATH=/home/fanyucai/lib/fftw/usr/lib64/:\$LD_LIBRARY_PATH && cd $odir/ && $python $xml2html -i output.xml -n report && rm -r output.xml pic && cd -");
