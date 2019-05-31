import sys
out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene','ExonicFunc.refGene','AAChange.refGene','cytoBand',
          'avsnp150','ExAC_ALL','ExAC_EAS','esp6500siv2_all','1000g2015aug_all','1000g2015aug_eas','genome_AF','genome_AF_eas','exome_AF','exome_AF_eas',
          'cosmic88_coding','CLNALLELEID','CLNDN','CLNDISDB','CLNREVSTAT','CLNSIG','SIFT_pred','Polyphen2_HDIV_pred', 'Polyphen2_HVAR_pred','MutationTaster_pred','MutationAssessor_pred','FATHMM_pred',
          'CADD_phred','InterVar_automated','UMT','VMT','VMF']
def all(annovar,genelist,out):
    dict = {}
    infile = open(genelist, "r")
    for line in infile:
        line = line.strip()
        dict[line] = 1
    infile.close()
    infile = open(annovar, "r")
    outfile = open("%s.filter.annovar.all" % (out), "w")
    for line in infile:
        line = line.strip()
        array = line.split("\t")
        if array[8]=="synonymous SNV" or array[5]=="intronic" or array[5]=="intergenic" or array[5].startswith("UTR"):
            continue
        else:
            if array[6] in dict:
                outfile.write("%s\n" % (line))
    infile.close()
    outfile.close()

if __name__=="__main__":
    if len(sys.argv)!=4:
        print("Usage:\npython3 filter_all.py annovarfile genelist outdir/prefix")
        print("Copyright:fanyucai")
        print("Version:1.0")
        sys.exit(-1)
    all(sys.argv[1],sys.argv[2],sys.argv[3])