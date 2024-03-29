##Plot scatter plot for KEGG pathway enrichment analysis
args <-commandArgs(TRUE);##sampleName ##output dir ##identify file
library(ggplot2)
path=read.table(args[3],sep="\t",header=T)
colnames(path)<-c("Pathway_term","Rich_factor","qvalue","Gene_number")
p<-ggplot(path, aes(Rich_factor,Pathway_term))
p<-p+geom_point(aes(colour=qvalue,size=Gene_number))+scale_colour_gradientn(colours=rainbow(4),guide = "colourbar") +expand_limits(color=seq(0, 1, by=0.25))
p<-p+ggtitle(paste ("Statistics of Pathway Enrichment (",args[1],")",sep="")) + xlab("Rich factor") +ylab("")
p<-p+theme_bw()+theme(axis.text=element_text( color="black", size=10))
p<-p+theme(panel.border=element_rect(colour = "black"))
p<-p+theme(plot.title=element_text(vjust=1), legend.key=element_blank())
p
ggsave(paste(args[2],"/",args[1],".","KEGG_pathway_enrichment_scatterplot.png",sep=""), plot=p,type="cairo-png", width=8, height=7, dpi=700)
ggsave(paste(args[2],"/",args[1],".","KEGG_pathway_enrichment_scatterplot.pdf",sep=""), plot=p, width=8, height=7)
