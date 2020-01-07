import os

root_file="/data/Rawdata/Nuohe"
filename=["TS19445TF","TS19446TF","TS19447TF","TS19448TF","TS19449TF","TS19450TF","TS19451TF","TS19452TF","TS19453TF","TS19454TF","TS19455TF","TS19456TF","TS19457TF","TS19458TF","TS19459TF","TS19460TF"]

for(root,dirs,files) in os.walk(root_file):
    for file in files:
        tmp=os.path.join(root,file)
        if tmp.endswith(".fq.gz"):
            samplename = tmp.split("/")[-1].split("_")[0]
            if samplename.replace('-R',"") in filename:
                print(tmp)