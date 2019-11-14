import os
root_dir="/data/TSO500/"

sampleID_line=0
TMB_line=0
MSI_line=0
sampleID={}
for root,dirs,files in os.walk(root_dir):
    for file in files:
        tmp=os.path.join(root,file)
        if tmp.endswith("MetricsReport.tsv"):
            infile=open(tmp,"r")
            num=0
            sample_name=[]
            for line in infile:
                num+=1
                line=line.strip()
                array=line.split("\t")
                if line.startswith("[DNA Library QC Metrics]"):  #######get the sampleID
                    sampleID_line=num
                if num==sampleID_line+1:
                    for i in range(3,len(array)):
                        sample_name.append(array[i])
                if num == sampleID_line + 2:
                    for i in range(3, len(array)):
                        if float(array[i])>3106:
                            if not sample_name[i - 3] in sampleID:
                                sampleID[sample_name[i-3]]="CONTAMINATION_SCORE"
                            else:
                                sampleID[sample_name[i - 3]] += "CONTAMINATION_SCORE"
                if line.startswith("[DNA Library QC Metrics for Small Variant Calling and TMB]"):
                    TMB_line=num+2
                if num == TMB_line+1:
                    for i in range(3, len(array)):
                        if float(array[i])<150:
                            if not sample_name[i - 3] in sampleID:
                                sampleID[sample_name[i - 3]] = "MEDIAN_EXON_COVERAGE"
                            else:
                                sampleID[sample_name[i - 3]] += "\tMEDIAN_EXON_COVERAGE"
                if num == TMB_line + 2:
                    for i in range(3, len(array)):
                        if float(array[i]) < 90:
                            if sample_name[i - 3] in sampleID:
                                sampleID[sample_name[i - 3]] += "\tPCT_EXON_50X"
                            else:
                                sampleID[sample_name[i - 3]] = "PCT_EXON_50X"
                if line.startswith("[DNA Library QC Metrics for MSI]"):
                    MSI_line=num+2
                if num==MSI_line:
                    for i in range(3, len(array)):
                        if float(array[i]) < 40:
                            if sample_name[i - 3] in sampleID:
                                sampleID[sample_name[i - 3]] += "\tmsi"
                            else:
                                sampleID[sample_name[i - 3]] = "msi"
outfile=open("/data/TSO500/stat/unqualified_sample_name.tsv","w")
for key in sampleID:
    outfile.write("%s\t%s\n"%(key,sampleID[key]))