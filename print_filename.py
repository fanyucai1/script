import os

root_file="/data/Rawdata/Nuohe"
filename=["TS19461TF",
"TS19462TF",
"TS19463TF",
"TS19464TF",
"TS19465TF",
"TS19466TF",
"TS19467TF",
"TS19468TF",
"TS19469TF",
"TS19470TF",
"TS19471TF",
"TS19472TF",
"TS19473TF",
"TS19474TF",
"TS19475TF",
"TS19476TF",
"TS19477TF",
"TS19478TF",
"TS19479TF",
"TS19480TF",
"TS19481TF",
"TS19482TF",
"TS19483TF",
"TS19484TF",
"TS19485TF",
"TS19486TF",
"TS19487TF",
"TS19488TF",
"TS19489TF",
"TS19490TF",
"TS19491TF",
"TS19492TF",
"TS19493TF",
"TS19494TF",
"TS19495TF",
"TS19496TF"]
for(root,dirs,files) in os.walk(root_file):
    for file in files:
        tmp=os.path.join(root,file)
        if tmp.endswith(".fq.gz"):
            samplename = tmp.split("/")[-1].split("_")[0]
            if samplename.replace('-R',"") in filename:
                print(tmp)