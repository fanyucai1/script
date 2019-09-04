import os
import sys
import subprocess

out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene','ExonicFunc.refGene','AAChange.refGene','cytoBand',
          'avsnp150','snp138','ExAC_ALL','esp6500siv2_all','1000g2015aug_all','genome_AF','exome_AF',
          'cosmic88_coding','CLNALLELEID','CLNDN','CLNDISDB','CLNREVSTAT','CLNSIG','InterVar_automated','Canonical_transcript','SIFT_pred','Polyphen2_HDIV_pred', 'Polyphen2_HVAR_pred','MutationTaster_pred','MutationAssessor_pred','FATHMM_pred',
          'CADD_phred','FORMAT']
annovar="/software/docker_tumor_base/Resource/Annovar/"
def run(vcf,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    outfile=open("%s.annovar.tsv","w")
    output={}

    infile=open(vcf,"r")
    for line in infile:
        line=line.strip()
        if not line.startswith("#"):
            array=line.split("\t")
            output['Chr']=array[0]
            output['Start']=array[1]
            output['end']=int(array[1])+len(array[4])-len(array[3])

