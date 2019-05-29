import os
import argparse
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn2_circles
from matplotlib_venn import venn3, venn3_circles
import seaborn as sns
sns.set(style="ticks")
parser=argparse.ArgumentParser("This script will plot venn between two(three) vcf files .")
parser.add_argument("-v1","--vcf1",help="vcf file",required=True)
parser.add_argument("-l1","--label1",help="label",required=True)
parser.add_argument("-v2","--vcf2",help="vcf file",required=True)
parser.add_argument("-l2","--label2",help="label",required=True)
parser.add_argument("-v3","--vcf3",help="vcf file")
parser.add_argument("-l3","--label3",help="label")
args=parser.parse_args()
args.vcf1=os.path.abspath(args.vcf1)
args.vcf2=os.path.abspath(args.vcf2)
file1=open(args.vcf1,"r")
list1=[]
for line in file1:
    if not line.startswith("#"):
        line=line.strip()
        array=line.split()
        tmp=array[0]+array[1]+array[3]+array[4]
        list1.append(tmp)
file2=open(args.vcf2,"r")
list2=[]
for line in file2:
    if not line.startswith("#"):
        line=line.strip()
        array=line.split()
        tmp=array[0]+array[1]+array[3]+array[4]
        list2.append(tmp)
if args.vcf3:
    file3=open(args.vcf3,"r")
    list3=[]
    for line in file3:
        if not line.startswith("#"):
            line = line.strip()
            array = line.split()
            tmp = array[0] + array[1] + array[3] + array[4]
            list3.append(tmp)
    set1 = set(list1)
    set2=set(list2)
    set3=set(list3)
    venn3([set1, set2, set3], set_labels=(args.label1, args.label2,args.label3))
else:
    set1 = set(list1)
    set2 = set(list2)
    venn2([set1, set2], set_labels=(args.label1, args.label2))
plt.title("Sample Venn diagram")
plt.savefig("venn.png",dpi=300)