
import sys
import os
import xlrd
import xlsxwriter
database = ['1000g2015aug_all','1000g2015aug_eas', 'ExAC_ALL', 'esp6500siv2_all','ExAC_EAS','genome_AF','genome_AF_eas','exome_AF','exome_AF_eas']
out_name=['Chr','Start','End','Ref','Alt','Func.refGene','Gene.refGene','GeneDetail.refGene',
          'ExonicFunc.refGene',	'AAChange.refGene',	'cytoBand',	'1000g2015aug_all',	'avsnp150',	'snp138',
          'CLNALLELEID','CLNDN','CLNDISDB',	'CLNREVSTAT','CLNSIG','cosmic88_coding','SIFT_score','SIFT_pred',
          'Polyphen2_HDIV_score','Polyphen2_HDIV_pred','esp6500siv2_all','ExAC_ALL','ExAC_EAS','1000g2015aug_eas',
          '1000g2015aug_sas','1000g2015aug_afr','1000g2015aug_amr','1000g2015aug_eur','InterVar_automated','GT','AAChange.1',
          'Ref_Reads',	'Alt_Reads','Var']
cosmic_vcf="/data/Database/COSMIC/release_v88/CosmicCodingMuts.hg19.vcf"
maf=0.01
##############################################
def germline(maf,annovar,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    in_workbook = xlrd.open_workbook(annovar)
    in_sheet = in_workbook.sheet_by_index(0)
    out_workbook = xlsxwriter.Workbook('%s.annovar.filter.xlsx' % (out))
    out_worksheet = out_workbook.add_worksheet()
    for i in range(len(out_name)):
        out_worksheet.write(0,i,out_name[i])
    line_num=0
    for k in range(1,in_sheet.nrows):
        if in_sheet.cell(k,8)=="synonymous SNV":
            continue
        elif in_sheet.cell(k,5)=="intronic" or in_sheet.cell(k,5)=="intergenic":
            continue
        else:
            freq = 0
            freq_counts = 0
            result = "false"
            for j in range(0,in_sheet.ncols):
                if in_sheet.cell(0,j)=="CLNSIG" or in_sheet.cell(0,j)=="InterVar_automated":
                    if in_sheet.cell(k,j)=="Pathogenic":
                        result = "true"
                    if in_sheet.cell(k,j)=="Likely_pathogenic":
                        result = "true"
                    if in_sheet.cell(k,j)=="drug_response":
                        result = "true"
                    if in_sheet.cell(k,j)=="Likely pathogenic":
                        result = "true"
                    for n in database:
                        if in_sheet.cell(0, j)==n:
                            if in_sheet.cell(k,j)!=".":
                                if float(in_sheet.cell(k,j))<= float(maf):
                                    freq += 1
                                else:
                                    freq_counts += 1
                            else:
                                pass
                    if freq_counts < 3:# not common snp
                        if freq >= 1:  # at least 1<MAF
                            result = "true"
            if result == "true":
                line_num+=1
                for l in range(len(out_name)):
                    out_worksheet.write(line_num, l, in_sheet.cell(line_num,l))
        out_workbook.close()

if __name__=="__main__":
    if len(sys.argv)!=5:
        print("Usage:\npython3 filter_germline.py maf annovarfile outdir prefix")
        print("Copyright:fanyucai")
        print("Version:1.0")
        sys.exit(-1)
    germline(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])