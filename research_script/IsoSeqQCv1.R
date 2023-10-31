#####################################################################
# Copyright 2015, BMK
# Promgrame: IsoSeq_QC_Stat
# Author: tengh <tengh@biomarker.com.cn>
# Date: 20151012
# Function:Pacbio cDNA sequencing data IsoSeq result QC anlysis 
#
#####################################################################
#computes and plot a histogram of the given data values
single.hist<-function(x,outfile="hist",xlim=range(x),binwidth=NULL,is.smooth=NULL,height=3000,width=4000,xlab="",ylab="",lab.size=14,axis.size=14,title="",line.color=4,linetype=1,line.size=1,hist.color=2,no.grid=T){
  x<-x[!is.na(x)]
  df <- data.frame(x=as.numeric(x))
  #-----------------------------------------------------------------
  # plot
  #-----------------------------------------------------------------
  # mian plot
  p <- ggplot(df, aes(x=x))
  # good color
  colorSet <- c("#E41A1C","#377EB8","#4DAF4A","#984EA3","#FF7F00","#FFFF33","#A65628","#F781BF","#999999")
  if(is.numeric(hist.color) && hist.color<=9 && hist.color>0){
    hist.color=colorSet[hist.color]
  }
  
  if(is.numeric(line.color)&&line.color>0 &&line.color<=9){
    line.color=colorSet[line.color]
  }
  # binwidth
  if(is.null(binwidth)){
    binwidth <- ( range(df$x)[2] - range(df$x)[1] ) / 30
  }
  # hist
  if( is.null(is.smooth) ){
    p <- p + geom_histogram(colour="white", fill=hist.color, binwidth=binwidth)
    # desinty
  }else{
    p <- p + geom_histogram(aes(y = ..density..), colour="white", fill=hist.color, binwidth=binwidth)
    p <- p + geom_line(aes(y = ..density..), colour =line.color, size=line.size, linetype=linetype, stat = 'density')
  }
  # xlim
  if(is.null(xlim)){
    xlim=range(data)
  }else if(length(xlim)!=2||xlim[2]<xlim[1]){
    warning("hist plot Error[xlim]:xlim must be NULL or a numeric vector of length 2, reset xlim=range(data)!")
  }
  p <- p + xlim(xlim[1], xlim[2])
  
  #-----------------------------------------------------------------
  # theme
  #-----------------------------------------------------------------
  # lab
  p <- p + xlab(xlab) + ylab(ylab) + labs(title=title)
  # set lab and axis test size
  p <- p + theme(title = element_text(face="bold", size=lab.size), 
                 axis.text = element_text(face="bold", size=axis.size,color = "black"))
  # remove legend
  p <- p + theme(legend.position = "none")
  # grid and background
  if ( !is.null(no.grid) ) {
    p <- p + theme( panel.background = element_rect(colour="black", size=1, fill="white"),
                    panel.grid =  element_line(colour = "#CCCCCC"))
  }
  
  
  
  #-----------------------------------------------------------------
  # output plot
  #-----------------------------------------------------------------
  pdf(file=paste(outfile,".pdf",sep=""), height=height*2/1000, width=width*2/1000)
  print(p)
  dev.off()
  png(filename=paste(outfile,".png",sep=""), height=height, width=width, res=500, units="px")
  print(p)
  dev.off()
}


library(getopt)
library(R.utils)
#+--------------------
# get options
#+--------------------
spec <- matrix(c(
  'help', 'h', 0, "logical", "help",
  'input','i',1,"character", "[forced] A character vector (of arbitrary length when reading, of length 1 when writing) containing the path(s) to the file(s) to read or write. Reading files in gzip format (which usually have the '.gz' extension) is supported.",
  'output', 'o', 1, "character", "[forced] output png file path",
  'format','f',2,"character","[optional] Either <fasta> (the default) or <fastq>",
  'x.title', 'x', 2, "character", "[optional] x title, default [Read Length].",
  'y.title', 'y', 2, "character", "[optional] y title, default [Reads].",
  'title', 't', 2, "character", "[optional] graph title, default [\'\']",
  'size','s',2,'integer',"[optional] fontsize of lab and title text,default[16]",
  'bg','b',2,"logical","[optional] plot background or not[FALSE]",
  'width','W',2,"integer","[optional] graph width default[4000]",
  'height','H',2,"integer","[optional] graph height default[3000]"
), byrow = TRUE, ncol = 5)
opt <- getopt(spec)
#+--------------------
# check options
#+--------------------
if ( !is.null(opt$help) | is.null(opt$input) |is.null(opt$output)) {
  cat(getopt(spec, usage=TRUE))
  q(status=1)
}

#opt<- data.frame(input="reads_of_insert.fasta",output="E:/R_workplace/20150902SMRTplot/reads_of_insert")
#################check forced options
input<-as.vector(opt$input)
if(file.exists(input)){
  input=getAbsolutePath(input)
}else{
  stop("Error:input file not exist!")
}

output<-as.vector(opt$output)
output=getAbsolutePath(output)
if(!file.exists(dirname(output))){
  output=dir.create(dirname(output),recursive=T)
}

#+--------------------
# some default options
#+--------------------

if ( is.null(opt$format) ) opt$format <- "fasta"
if ( is.null(opt$x.title) ) opt$x.title <- "Read Length"
if ( is.null(opt$y.title) ) opt$y.title <- "Reads"
if ( is.null(opt$title) ) opt$title <- ""
if ( is.null(opt$bg) ) opt$bg <- FALSE
if ( is.null(opt$width) ) opt$width <- 4000
if ( is.null(opt$height) ) opt$height <- 3000
if ( is.null(opt$size) ) opt$size <- 8
#+--------------------
# Main
#+--------------------

## load ggplot2 
library(ggplot2)
library(Biostrings)

## Improt data
DNA<-readDNAStringSet(filepath =input,format =opt$format )
DNA.seqlen<-width(DNA)
single.hist(x=DNA.seqlen,outfile=paste(output,".png",sep =""),binwidth =500,xlab=opt$x.title,ylab=opt$y.title,lab.size =opt$size,axis.size =opt$size)
ReadsNum<-length(DNA)
BaseNum<-sum(DNA.seqlen)
AverageLen<-mean(DNA.seqlen)
minLen<-min(DNA.seqlen)
maxLen<-max(DNA.seqlen)
stsFile=paste(dirname(output),"/QC.stat",sep ="")
if(file.exists(stsFile)){
  write.table(x = data.frame(DataType=basename(output),ReadsNum=ReadsNum,BaseNum=BaseNum,AverageLen=AverageLen,minLen=minLen,maxLen=maxLen),file = stsFile,append = T,sep="\t",row.names=F,col.names=F)
}else{
  write.table(x = data.frame(DataType=basename(output),ReadsNum=ReadsNum,BaseNum=BaseNum,AverageLen=AverageLen,minLen=minLen,maxLen=maxLen),file = stsFile,append = F,sep="\t",row.names=F,col.names=T)
}