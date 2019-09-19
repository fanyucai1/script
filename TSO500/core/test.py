outfile=open("SampleSheet.csv","w")
outfile.write("""[Header]
IEMFileVersion,4
Investigator Name,User Name
Experiment Name,Experiment
Date,2019/8/1
Workflow,From GenerateFASTQ
Application,NextSeq FASTQ Only
Assay
Description
Chemistry,Default

[Reads]
151
151

[Settings]
Adapter,AGATCGGAAGAGCACACGTCTGAACTCCAGTCA
AdapterRead2,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT
Read1UMILength,7
Read2UMILength,7
Read1StartFromCycle,9
Read2StartFromCycle,9

[Data]
Sample_ID,Sample_Name,Sample_Plate,Sample_Well,Index_ID,index,I7_Index_ID,index2,I5_Index_ID
""")