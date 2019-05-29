#Email:fanyucai1@126.com
#2019.3.13
import argparse
import pandas as pd
import subprocess
import os
import pymrmr
blca="/home/fanyucai/low_CNV/test_data/blca_CNA_data.txt"
ucec="/home/fanyucai/low_CNV/test_data/ucec_CNA_data.txt"
print("blca download from: http://cbio.mskcc.org/cancergenomics/pancan_tcga/cna/blca_CNA_data.txt")
print("ucec downloda from: http://cbio.mskcc.org/cancergenomics/pancan_tcga/cna/ucec_CNA_data.txt")
out=pd.DataFrame()

df = pd.read_csv(blca,sep="\t")
data=df.T
data=data.iloc[3:,]
print("blca contains %s samples and %s genes" %(data.shape[0],data.shape[1]))
data.insert(0,'class',0)
out=out.append(data)


df = pd.read_csv(ucec,sep="\t")
data=df.T
data=data.iloc[3:,]
print("ucec contains %s samples and %s genes" %(data.shape[0],data.shape[1]))
data.insert(0,'class',1)
out=out.append(data)
out=out.reset_index(drop=True)
out.columns="v"+out.columns.astype(str)
out=out.rename(columns={'vclass':'class'})
df=pymrmr.mRMR(out, 'MIQ', 10)
out.to_csv("/home/fanyucai/low_CNV/test_data/CNV.csv",sep="\t",index=False)

q=pymrmr.mRMR(df, 'MIQ', 30)
print(q)
