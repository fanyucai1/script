import sys
out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene','ExonicFunc.refGene','AAChange.refGene','cytoBand',
          'avsnp150','ExAC_ALL','ExAC_EAS','esp6500siv2_all','1000g2015aug_all','1000g2015aug_eas','genome_AF','genome_AF_eas','exome_AF','exome_AF_eas',
          'cosmic88_coding','CLNALLELEID','CLNDN','CLNDISDB','CLNREVSTAT','CLNSIG','SIFT_pred','Polyphen2_HDIV_pred', 'Polyphen2_HVAR_pred','MutationTaster_pred','MutationAssessor_pred','FATHMM_pred',
          'CADD_phred','InterVar_automated','UMT','VMT','VMF']
def split_gene(genelist,annovar,out):
    dict = {}
    infile = open(genelist, "r")
    for line in infile:
        line = line.strip()
        dict[line] = 1
    infile.close()
    infile = open(annovar, "r")
    outfile = open(out, "w")
    for i in range(len(out_name)):
        if i == 0:
            outfile.write("%s" % (out_name[i]))
        else:
            outfile.write("\t%s" % (out_name[i]))
    outfile.write("\n")
    num = 0
    for line in infile:
        line = line.strip()
        num += 1
        if num == 1:
            outfile.write("%s\n" % (line))
        else:
            array = line.split()
            if array[6] in dict:
                outfile.write("%s\n" % (line))
    infile.close()
    outfile.close()

if __name__=="__main__":
    if len(sys.argv)!=4:
        print("python split.py genelist annovarfile outfile\n")
        sys.exit(-1)
    genelist=sys.argv[1]
    annovar=sys.argv[2]
    out=sys.argv[3]
    split_gene(genelist,annovar,out)