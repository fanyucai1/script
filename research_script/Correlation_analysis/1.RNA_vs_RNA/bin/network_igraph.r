#!/usr/bin/env Rscript
suppressPackageStartupMessages(library("optparse"))
option_list = list(
        make_option(c("-e", "--edges"), type="character", default=NULL, help="The input edges", metavar="character"),
	make_option(c("-n", "--nodes"), type="character", default=NULL, help="The input nodes", metavar="character"),
        make_option(c("-o", "--picname"), type="character", default=NULL, help="output picture name", metavar="character")
       );
opt_parser = OptionParser(option_list=option_list,epilogue = "Rscript network_igraph.r -e R3_vs_R0.miRNA_mRNA.edges.xls -n R3_vs_R0.miRNA_mRNA.nodes.xls -o R3_vs_R0.miRNA_mRNA");
opt = parse_args(opt_parser);
if (is.null(opt$edges) | is.null(opt$nodes) | is.null(opt$picname)){
	print_help(opt_parser)
	stop("--edges --nodes --picname must be supplied", call.=FALSE)
}

suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(network))
suppressPackageStartupMessages(library(GGally))
suppressPackageStartupMessages(library(sna))
suppressPackageStartupMessages(library(scales))
suppressPackageStartupMessages(library(RColorBrewer))

links<-read.table(opt$edges, header=T, sep="\t", check.names=F, quote="", na.strings = "", comment.char = "")
nodes<-read.table(opt$nodes, header=T, sep="\t", check.names=F, quote="", na.strings = "", comment.char = "")
em.net<-as.matrix(links)
nodes<-as.matrix(nodes)
color<-as.character(nodes[,3])
color[which(nodes[,3]=="down")]="green"
color[which(nodes[,3]=="up")]="red"
type<-as.character(nodes[,2])
type[which(nodes[,2]=="miRNA")]=17
type[which(nodes[,2]!="miRNA")]=16
type<-as.numeric(type)
degree<-as.numeric(nodes[,4])
names(color)=nodes[,1]
names(type)=nodes[,1]
names(degree)=nodes[,1]

em.net <- network::network(em.net, directed = F)
network::set.vertex.attribute(em.net,"color",color[network.vertex.names(em.net)])
network::set.vertex.attribute(em.net,"type",type[network.vertex.names(em.net)])
network::set.vertex.attribute(em.net,"degree",sqrt(0.3*(degree[network.vertex.names(em.net)]+2)))
network::set.vertex.attribute(em.net,"size",sqrt(0.3*(sna::degree(em.net)+1)))
color<-factor(get.vertex.attribute(em.net,"color"),levels=c("red", "green"))


p<-ggnet2(em.net, node.color="color",shape="type", 
       layout.exp = 0.5,
       #layout.par = list(niter=1000,cell.jitter =1),
       size = "degree",label=TRUE,label.size=2.5,label.color="#515151",vjust=0,
       edge.alpha = 1,edge.size=0.2,edge.color="#63B8FF",
       #color.legend = "color", 
       alpha=0.9,
       mode= "fruchtermanreingold",
       legend.position = "none",legend.size="size")

ggsave(paste0(opt$picname, ".pdf"),width=8,height=8,plot=p)
ggsave(paste0(opt$picname, ".png"),type="cairo-png",width=8,height=8,plot=p)
