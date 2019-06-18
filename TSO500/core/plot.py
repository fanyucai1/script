import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import seaborn as sns

df=pd.read_table("TMB_MSI.tsv",sep="\t",header=0)
x=df['Total_TMB']
y=df['Cancer']
plt.figure(figsize=(18, 10))
sns.boxplot(x,y,data=df)
plt.savefig('out.png',dpi=300)