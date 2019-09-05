#Email:fanyucai1@126.com
#2019.5.23
import os
import argparse
import sys
sub=os.path.abspath(__file__)
dir_name=os.path.dirname(sub)
sys.path.append(dir_name)
import core
import time
import shutil

parser=argparse.ArgumentParser("Run 275 panel analysis.")
parser.add_argument("-p1","--pe1",help="tumor 5 reads",required=True)
parser.add_argument("-p2","--pe2",help="tumor 3 reads",required=True)
parser.add_argument("-n1","--n1",help="normal 5 reads",default="0")
parser.add_argument("-n2","--n2",help="normal 3 reads",default="0")
parser.add_argument("-p","--prefix",help="prefix output",required=True)
parser.add_argument("-o","--outdir",help="output directory",required=True)
parser.add_argument("-g","--genelist",help="gene list",required=True)
parser.add_argument("-m","--maf",help="maf",choices=[0.01],default=0.01,type=float)
parser.add_argument("-t","--type",help="sample type",choices=["tissue","ctDNA"],required=True)
parser.add_argument("-s","--sex",help="sex",choices=["male","female"],required=True)
parser.add_argument("-b","--bed",help="bed file",default="/data/Panel275/bed/DHS-3501Z.roi.bed")
args=parser.parse_args()
start=time.time()
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)
out=args.outdir+"/"+args.prefix
a=args.pe1
b=args.pe2
c=args.n1
d=args.n2
purity=0
vaf=0
if args.type=="tissue":
    vaf=0.02
    purity=0.1
else:
    purity=0.01
    vaf = 0.005
#####################################################################run docker
core.print_config.tumor_only(a, b, args.prefix, args.outdir,purity,args.sex,args.type,c,d)
if c=="0" and d=="0":
    #####################################################################filter VAF and genelist
    core.prefilter.run("%s.smCounter.anno.vcf"%(out),args.genelist,vaf,args.outdir,args.prefix)
    #####################################################################split germline and somatic
    core.germline_somatic.run_split("%s.vaf.%s.vcf" % (out, vaf), args.outdir, args.prefix)
else:
    core.tumor_normal.run("%s.smCounter.anno.vcf"%(out),args.genelist,vaf,args.outdir,args.prefix)
######################################################################anno vcf and filter vcf
if not os.path.exists("%s/result/"%(args.outdir)):
    os.mkdir("%s/result/"%(args.outdir))
if not os.path.exists("%s/result/SNV"%(args.outdir)):
    os.mkdir("%s/result/SNV"%(args.outdir))
core.annovar275.run("%s.germline.vcf"%(out),"%s"%(args.outdir),"%s.germline"%(args.prefix))
core.annovar275.run("%s.somatic.vcf"%(out),"%s"%(args.outdir),"%s.somatic"%(args.prefix))
shutil.copy("%s.germline.annovar.tsv"%(out), "%s/result/SNV/"%(args.outdir))
shutil.copy("%s.somatic.annovar.tsv"%(out), "%s/result/SNV/"%(args.outdir))
core.filter_somatic.somatic(args.maf,"%s.somatic.annovar.tsv"%(out),"%s/result/SNV/"%(args.outdir),"%s.somatic"%(args.prefix))
core.filter_germline.germline(args.maf,"%s.germline.annovar.tsv"%(out),"%s/result/SNV/"%(args.outdir),"%s.germline"%(args.prefix))
if c=="0" and d=="0":
    core.annovar275.run("%s.unknow.vcf"%(out),"%s"%(args.outdir),"%s.unknow"%(args.prefix))
    shutil.copy("%s.unknow.annovar.tsv" % (out), "%s/result/SNV/" % (args.outdir))
    core.filter_somatic.somatic(args.maf, "%s.unknow.annovar.tsv" % (out), "%s/result/SNV/" % (args.outdir),"%s.unknow" % (args.prefix))
######################################################################MSI
if args.type=="tissue":
    if not os.path.exists("%s/result/MSI" % (args.outdir)):
        os.mkdir("%s/result/MSI" % (args.outdir))
    if c == "0" and d == "0":
        core.MSI_tumor_only.run_msi("%s.bam"%(out),"%s"%(args.outdir),"%s"%(args.prefix))
        shutil.copy("%s.msi.tsv"%(out),"%s/result/MSI/"%(args.outdir))
    else:
        core.MSI_pair.pairs("%s.bam"%(out),"%s/normal.bam"%(args.outdir),args.bed,20,args.outdir,args.prefix,0.05)
        shutil.copy("%s.MSI"%(out),"%s/result/MSI/%s.msi.tsv"%(args.outdir,args.prefix))
######################################################################run CNV and filter CNV gene list
if not os.path.exists("%s/result/CNV"%(args.outdir)):
    os.mkdir("%s/result/CNV"%(args.outdir))
core.cnv.run("%s.copy-number.vcf"%(out),args.sex,args.genelist,"%s/result/CNV"%(args.outdir),args.prefix)
######################################################################sample quality statistics
core.stat_qc.run(args.outdir,args.prefix)
######################################################################
end=time.time()
print("Elapse time is %g seconds" %(end-start))
core.twillo_run.run("275_%s"%(args.prefix))