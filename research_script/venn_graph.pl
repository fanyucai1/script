#!/home/fanyucai/software/perl/perl-v5.24.1/bin/perl
#wangxiaoyue 2018-03-23
use strict;
use warnings;
use Getopt::Long;
use File::Spec;
use File::Basename;
use FindBin qw($Bin);
use Cwd;

###################### software or env ###############################################################
my $env="export PATH=/home/fanyucai/software/gcc/gcc-v6.1.0/bin/:/home/fanyucai/software/R/R-v3.4.0/bin/:\$PATH";
$env.=" && export LD_LIBRARY_PATH=/home/fanyucai/software/gcc/gcc-v6.1.0/lib64/:\$LD_LIBRARY_PATH";
#### convert
chomp(my $who=`whoami`);
system("mkdir ~/.config/") unless -d "/home/$who/.config/";
system("cp -a /home/fanyucai/.config/ImageMagick ~/.config/") unless -d "/home/$who/.config/ImageMagick";
my $convert_env="export PATH=/home/fanyucai/lib/usr/bin/:\$PATH && export LD_LIBRARY_PATH=/home/fanyucai/lib/usr/lib64/:\$LD_LIBRARY_PATH";
$convert_env .= " && export MAGICK_CONFIGURE_PATH=/home/$who/.config/ImageMagick && ";
$convert_env .= "export MAGICK_CODER_MODULE_PATH=/home/fanyucai/lib/usr/lib64/ImageMagick-6.7.2/modules-Q16/coders";
######################################################################################################

my (@infile, $format, @labels, @colnum, $outdir, $method, $config, $help);
GetOptions(
	"i:s{1,}"   => \@infile,
	"f:s"       => \$format,
	"l:s{1,}"   => \@labels,
	"c:i{1,}"   => \@colnum,
	"o:s"       => \$outdir,
	"m:s"       => \$method,
	"s:s"       => \$config,
	"h|help!"   => \$help,
);

my $usage=<< "USAGE";
Program: $0
Description: draw venn graph 
Options:
	-i     <infile>    The input files                                                       [Required]
	-f     <str>       Inputfile format: matrix or sets. (default: matrix)                   [Optional]
	-l     <str>       The label names is shown on the venn graph when '-f' is sets          [Optional]
	                   default: labels is inputfile's names when there is no option '-l'
	-c     <str>       The inputfile specified columns is used draw venn                     [Optional]
	                   default: 1(for sets), all colnum(for matrix)
	-o     <outdir>    The output directory of result. (default: ./)                         [Optional]
	-m     <str>       Draw venn graph method: VennDiagram, UpSetR, Petals                   [Optional]
	                   default: VennDiagram(<=5), UpSetR(>5 && <=15), Petals(>15)
	-s     <infile>    color config file for 'Petals'                                        [Optional]
	                   Without this option, the color is the default color
	                   2 colnum(labels[tab]color):
	                   Group2-vs-Group1	#8470FF
	                   Group3-vs-Group2	#20B2AA
	-h|help            print help info
Example:
	perl venn_graph.pl -i file1.xls file2.xls file3.xls -f sets -l name1 name2 name3 -c 1 2 3 -o outdir/
	perl venn_graph.pl -i matrix.xls -c 2 3 4 5 -o outdir/

USAGE

die $usage if(!@infile || $help);
#(@infile==0) && die "Error: don't find infile !\n";
$format ||= "matrix";
if($format eq "sets"){
	@labels=map {my $tmp=basename($_); $tmp=~s/\.\w+$//; $tmp} @infile if(!@labels);
	@colnum=(1) if(!@colnum);
}
$outdir ||= getcwd;
if($format eq "matrix" && @labels){
	warn "Warn: matrix formart infile don't support option '-l' !!!\n";
	die $usage;
}
if($format eq "matrix" && @infile!=1){
	warn "Warn: infile number must be one when format is matrix !!!\n";
	die $usage;
}
if(@labels!=0 && @infile!=@labels){
	die "Error: input files numbers is not equal to label names numbers!!!\n";
}

#create output directory
(-d $outdir) || mkdir $outdir;
$outdir=File::Spec->rel2abs($outdir);

#check infile
for(my $i=0;$i<=$#infile;$i++){
	(-s $infile[$i]) || die "Error: don't find $infile[$i] !\n";
	$infile[$i]=File::Spec->rel2abs($infile[$i]);
}
if($config){
	(-s $config) || die "Error: don't find $config !\n";
	$config=File::Spec->rel2abs($config);
}

#Conversion colnum as index
@colnum=map {$_-1} @colnum if(@colnum);

if($format eq "sets"){
	my %data; my $id_symbol;
	#read infile for 'sets' format
	for(my $i=0; $i<@infile; $i++){
		open IN,"<$infile[$i]" || die $!;
		while(<IN>){
			chomp;
			next if(/^\s*$/);
			my @l=split /\t/;
			my $venn_id=join("\t",@l[@colnum]);
			if($.==1){
				$id_symbol=$venn_id if(! defined $id_symbol);
			}else{
				$data{$venn_id}{$labels[$i]}=1;
			}
		}
		close IN;
	}

	#print outfile table
	open OUT,">$outdir/VennData.xls" || die $!;
	open TMP,">$outdir/VennData.xls_tmp" || die $!;
	print OUT "$id_symbol\t".join("\t",@labels)."\n";
	$id_symbol=~s/\t/_/g;
	print TMP "$id_symbol\t".join("\t",@labels)."\n";
	for my $gene (sort keys %data){
		print OUT "$gene";
		my $gene_tmp=$gene; $gene_tmp=~s/\t/_/g;
		print TMP "$gene_tmp";
		for my $name (@labels){
			if(exists $data{$gene}{$name}){
				print OUT "\t$data{$gene}{$name}";
				print TMP "\t$data{$gene}{$name}";
			}else{
				print OUT "\t0";
				print TMP "\t0";
			}
		}
		print OUT "\n";
		print TMP "\n";
	}
	close OUT;
	close TMP;
	undef %data; undef $id_symbol;
}elsif($format eq "matrix"){
	open IN,"<$infile[0]" || die $!;
	open OUT,">$outdir/VennData.xls_tmp" || die $!;
	while(<IN>){
		chomp;
		next if(/^\s*$/);
		my @l=split /\t/; 
		if($.==1){
			@labels= map {$l[$_]} @colnum if(@colnum);
			@labels= @l[1..$#l] if(!@colnum);
			print OUT "$l[0]\t".join("\t",@labels)."\n";
		}else{
			if(@colnum){
				my $out=$l[0]."\t".join("\t",@l[@colnum]);
				print OUT "$out\n";
			}else{
				print OUT "$_\n";
			}
		}
	}
	close IN;
	close OUT;
}else{
	die "Error: option '-f' is errr !!!\n";
}

######################################## draw venn graph ###############################
if(@labels<=5){
	$method ||="VennDiagram";
}elsif(@labels>5 && @labels<=15){
	$method ||= "UpSetR";
}elsif(@labels > 15){
	$method ||= "Petals";
}
die "Error: don't choose VennDiagram for >5 data!\n" if(@labels>5 && $method eq "VennDiagram");

if($method=~/VennDiagram/i){
	&VennDiagram("$outdir/VennData.xls_tmp", $outdir);
}elsif($method=~/UpSetR/i){
	&UpSetR("$outdir/VennData.xls_tmp", $outdir);
	
}else{
	&Petals("$outdir/VennData.xls_tmp", $outdir, $config) if(defined $config);
	&Petals("$outdir/VennData.xls_tmp", $outdir) if(!defined $config);
}
system("rm $outdir/VennData.xls_tmp");


########## sub program ######################################

#VennDiagram
sub VennDiagram{
	my ($infile, $outdir)=@_;
	open R,">$outdir/draw_venn.r" || die $!;
	print R "#!/usr/bin/env Rscript\n";
	print R "data <- read.table(\"$infile\",sep=\"\\t\",header=T,quote=\"\",check.names=FALSE)\n";
	print R "InputList<-list()\nmylabel=colnames(data)[-1]
for(i in 2:length(colnames(data))){
	InputList[[i-1]]<-data[which(data[,i]==1),1]
	mylabel[i-1] <- paste0(mylabel[i-1], \"\n(\", length(InputList[[i-1]]), \")\")
}
names(InputList)<-mylabel
if(length(mylabel)==2){fillColor<-c(\"red\", \"orange\")}
if(length(mylabel)==3){fillColor<-c(\"red\", \"orange\", \"green\")}
if(length(mylabel)==4){fillColor<-c(\"red\", \"orange\", \"green\", \"blue\")}
if(length(mylabel)==5){fillColor<-c(\"red\", \"orange\", \"green\", \"blue\", \"magenta\")}

library(\"VennDiagram\")
venn.plot<-venn.diagram(InputList, filename=NULL, col=NA, cat.col=\"black\", fill=fillColor, alpha =0.50, cat.cex=1.2, cat.fontface=\"bold\", margin=0.2, scale=TRUE)

pdf(file = \"$outdir/VennGraph.pdf\", width=10, height=10)
grid.draw(venn.plot)
dev.off()
png(file = \"$outdir/VennGraph.png\", width=3000, height=3000, res=300)
grid.draw(venn.plot)
dev.off()
file.remove(dir(\".\", pattern=\"^VennDiagram.*log\$\"))\n";
	close R;
	system("$env && Rscript $outdir/draw_venn.r && rm $outdir/draw_venn.r");
}

#UpSetR
sub UpSetR{
	my ($infile, $outdir)=@_;
	open R,">$outdir/draw_venn.r" || die $!;
	print R "#!/usr/bin/env Rscript\n";
	print R "data <- read.table(\"$infile\",sep=\"\\t\",header=T,quote=\"\",check.names=FALSE)\n";
	print R "library(UpSetR)
datnum <- length(colnames(data))-1
pdf(\"$outdir/VennGraph.pdf\", width=14, height=7, onefile=F)
upset(data, nsets=datnum, nintersects=NA, number.angles=30, point.size=2, line.size=1, mainbar.y.label=\"Intersection gene number\", sets.x.label=\"Total gene number\", text.scale=c(1.3,1.3,1,1,1.3,1), mb.ratio=c(0.55, 0.45), order.by=\"freq\", show.numbers=\"yes\", sets.bar.color=rainbow(datnum))
dev.off()

png(\"$outdir/VennGraph.png\", width=4200, height=2100, res=300)
upset(data, nsets=datnum, nintersects=NA, number.angles=30, point.size=2, line.size=1, mainbar.y.label=\"Intersection gene number\", sets.x.label=\"Total gene number\", text.scale=c(1.3,1.3,1,1,1.3,1), mb.ratio=c(0.55, 0.45), order.by=\"freq\", show.numbers=\"yes\", sets.bar.color=rainbow(datnum))
dev.off()\n";
	close R;
	system("$env && Rscript $outdir/draw_venn.r && rm $outdir/draw_venn.r");
}

#Petals graph
sub Petals{
	my($infile, $outdir, $config)=@_;
	#system("perl $Petals_venn -tab $infile -prefix $outdir/VennGraph -opacity 0.8 -ellipse_la 380 -ellipse_ma 80 -circle_r 25 -font_size 23");
	my $prefix="$outdir/VennGraph";
	my @mylabels; my %color;
	if(defined $config){
		open G,"<$config" || die "Error: don't open cfg file: $config!\n";
		while(<G>){
			chomp;
			next if(/^#/ || /^\s*$/);
			my @l=split /\t/;
			$mylabels[@mylabels]=$l[0];
			$color{$l[0]}=$l[1];
		}
		close G;
	}

	open F,"<$infile" || die "Error: don't open infile:$infile!\n";
	my %unique;my $common_num=0;my @sample;
	while(<F>){
		chomp;
		next if(/^\s*$/);
		my @l=split /\t/;
		if($.==1){
			@sample=@l[1..$#l];
			die "Error: table file name number is not equal to config file !\n" if(@mylabels!=0 && @mylabels!=@sample);
		}else{
			my @ture;
			for(my $i=1;$i<@l;$i++){
				if($l[$i]==1){
					$ture[@ture]=$sample[$i-1];
				}
			}
			$common_num++ if(@ture==@sample);
			$unique{$ture[0]}++ if(@ture==1);
		}
	}
	close F;

	@mylabels=@sample if(!@mylabels);
	for my $t (@mylabels){
		$unique{$t}=0 if(!exists $unique{$t});
	}

	use SVG;
	my ($circle_r, $ellipse_la, $ellipse_ma, $opacity, $font_size) = (25, 380, 80, 0.6, 23);
	my $svg = SVG->new(width=>$ellipse_la*2+600, height=>$ellipse_la*2+600);
	my $x0 = $ellipse_la+300; my $y0 = $ellipse_la+300;
	my $rx = $ellipse_la/2; my $ry = $ellipse_ma/2;

	my $n=@mylabels;
	for(my $i=0;$i<$n;$i++){
		my ($cx,$cy,$angle,$text_x,$text_y,$label_x,$label_y,$ellipse_col,$col_dafult);
		my $offset=1;my $sample_length = length($mylabels[$i]);
		if(360*$i/$n>=0 && 360*$i/$n<90){
			$col_dafult = (360*$i/$n<45) ? "#8470FF" : "#20B2AA";
			$cx = $x0+($rx-$circle_r)*sin(6.28*$i/$n);
			$cy = $y0-($rx-$circle_r)*cos(6.28*$i/$n);
			$angle = 360*$i/$n-90;
			if(exists $color{$mylabels[$i]}){$ellipse_col=$color{$mylabels[$i]};}else{$ellipse_col=$col_dafult;}
			$svg->ellipse(cx => $cx, cy => $cy, rx => $rx, ry => $ry, transform => "rotate($angle $cx $cy)", style=>{stroke=>'black','stroke-width',0,fill=>"$ellipse_col",'fill-opacity'=> "$opacity"});
			$text_x = $x0+($ellipse_la-3*$circle_r)*sin(6.28*$i/$n);
			$text_y = $y0-($ellipse_la-3*$circle_r)*cos(6.28*$i/$n);
			$offset=$offset*$sample_length/9 if((90-360*$i/$n)<=20);
			$svg->text(x => $text_x, y => $text_y, 'font-size'=>$font_size, 'text-anchor'=>'middle', 'stroke', 'black', 'stroke-width',0, '-cdata', $unique{$mylabels[$i]});
			$label_x=$x0+($ellipse_la+$offset)*sin(6.28*$i/$n);
			$label_y=$y0-($ellipse_la+$offset)*cos(6.28*$i/$n);
			$svg->text(x => $label_x, y => $label_y, transform => "rotate($angle $label_x $label_y)", 'font-size'=>5+$font_size, 'text-anchor'=>'start', 'stroke', 'black', 'stroke-width',0, '-cdata', "$mylabels[$i]");
		}elsif(360*$i/$n>=90 && 360*$i/$n<180){
			$col_dafult = (360*$i/$n<135) ? "#EE3B3B" : "#00BFFF";
			$cx = $x0+($rx-$circle_r)*sin(3.14-6.28*$i/$n);
			$cy = $y0+($rx-$circle_r)*cos(3.14-6.28*$i/$n);
			$angle = 90-(180-360*$i/$n);
			if(exists $color{$mylabels[$i]}){$ellipse_col=$color{$mylabels[$i]};}else{$ellipse_col=$col_dafult;}
			$svg->ellipse(cx => $cx, cy => $cy, rx => $rx, ry => $ry, transform => "rotate($angle $cx $cy)", style=>{stroke=>'black','stroke-width',0,fill=>"$ellipse_col",'fill-opacity'=> "$opacity"});
			$text_x = $x0+($ellipse_la-3*$circle_r)*sin(3.14-6.28*$i/$n);
			$text_y = $y0+($ellipse_la-3*$circle_r)*cos(3.14-6.28*$i/$n);
			$offset=$offset*$sample_length/9 if((360*$i/$n-90)<=20);
			$svg->text(x => $text_x, y => $text_y, 'font-size'=>$font_size, 'text-anchor'=>'middle', 'stroke', 'black', 'stroke-width',0, '-cdata', $unique{$mylabels[$i]});
			$label_x=$x0+($ellipse_la+$offset)*sin(3.14-6.28*$i/$n);
			$label_y=$y0+($ellipse_la+$offset)*cos(3.14-6.28*$i/$n);
			$svg->text(x => $label_x, y => $label_y, transform => "rotate($angle $label_x $label_y)", 'font-size'=>5+$font_size, 'text-anchor'=>'start', 'stroke', 'black', 'stroke-width',0, '-cdata', "$mylabels[$i]");
		}elsif(360*$i/$n>=180 && 360*$i/$n<270){
			$col_dafult = (360*$i/$n<225) ? "#FFA500" : "#00FF7F";
			$cx = $x0-($rx-$circle_r)*sin(6.28*$i/$n-3.14);
			$cy = $y0+($rx-$circle_r)*cos(6.28*$i/$n-3.14);
			$angle = 360*$i/$n-180-90;
			if(exists $color{$mylabels[$i]}){$ellipse_col=$color{$mylabels[$i]};}else{$ellipse_col=$col_dafult;}
			$svg->ellipse(cx => $cx, cy => $cy, rx => $rx, ry => $ry, transform => "rotate($angle $cx $cy)", style=>{stroke=>'black','stroke-width',0,fill=>"$ellipse_col",'fill-opacity'=> "$opacity"});
			$text_x = $x0-($ellipse_la-3*$circle_r)*sin(6.28*$i/$n-3.14);
			$text_y = $y0+($ellipse_la-3*$circle_r)*cos(6.28*$i/$n-3.14);
			$offset=$offset*$sample_length/9 if((270-360*$i/$n)<=20);
			$svg->text(x => $text_x, y => $text_y, 'font-size'=>$font_size, 'text-anchor'=>'middle', 'stroke', 'black', 'stroke-width',0, '-cdata', $unique{$mylabels[$i]});
			$label_x=$x0-($ellipse_la+$offset)*sin(6.28*$i/$n-3.14);
			$label_y=$y0+($ellipse_la+$offset)*cos(6.28*$i/$n-3.14);
			$svg->text(x => $label_x, y => $label_y, transform => "rotate($angle $label_x $label_y)", 'font-size'=>5+$font_size, 'text-anchor'=>'end', 'stroke', 'black', 'stroke-width',0, '-cdata', "$mylabels[$i]");
		}elsif(360*$i/$n>=270 && 360*$i/$n<=360){
			$col_dafult = (360*$i/$n<315) ? "#00FFFF" : "#FFFF00";
			$cx = $x0-($rx-$circle_r)*sin(6.28-6.28*$i/$n);
			$cy = $y0-($rx-$circle_r)*cos(6.28-6.28*$i/$n);
			$angle = 90-(360-360*$i/$n);
			if(exists $color{$mylabels[$i]}){$ellipse_col=$color{$mylabels[$i]};}else{$ellipse_col=$col_dafult;}
			$svg->ellipse(cx => $cx, cy => $cy, rx => $rx, ry => $ry, transform => "rotate($angle $cx $cy)", style=>{stroke=>'black','stroke-width',0,fill=>"$ellipse_col",'fill-opacity'=> "$opacity"});
			$text_x = $x0-($ellipse_la-3*$circle_r)*sin(6.28-6.28*$i/$n);
			$text_y = $y0-($ellipse_la-3*$circle_r)*cos(6.28-6.28*$i/$n);
			$offset=$offset*$sample_length/9 if((360*$i/$n-270)<=20);
			$svg->text(x => $text_x, y => $text_y, 'font-size'=>$font_size, 'text-anchor'=>'middle', 'stroke', 'black', 'stroke-width',0, '-cdata', $unique{$mylabels[$i]});
			$label_x=$x0-($ellipse_la+$offset)*sin(6.28-6.28*$i/$n);
			$label_y=$y0-($ellipse_la+$offset)*cos(6.28-6.28*$i/$n);
			$svg->text(x => $label_x, y => $label_y, transform => "rotate($angle $label_x $label_y)", 'font-size'=>5+$font_size, 'text-anchor'=>'end', 'stroke', 'black', 'stroke-width',0, '-cdata', "$mylabels[$i]");
		}
	}
	$svg->circle(cx => $x0, cy => $y0, r => $circle_r, style=>{stroke=>'black','stroke-width',0.5,fill=>"red",'fill-opacity'=> 0.92});
	$svg->text(x => $x0, y => $y0+($font_size-3)*6/15, 'font-size'=>$font_size-3, 'text-anchor'=>'middle', 'stroke', 'black', 'stroke-width',0, '-cdata', "$common_num");
	my $out = $svg->xmlify;
	open SVGFILE,">$prefix\.svg" || die $!;
	print SVGFILE $out;
	close SVGFILE;
	system("$convert_env && convert $prefix\.svg -quality 92 $prefix\.png");
}
