import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import seaborn as sns

df=pd.read_table("TMB_MSI.tsv",sep="\t",header=0)
x=df['Total_TMB']
y=df['Cancer']
fig, axs = plt.subplots()
plt.figure(figsize=(18, 10))
axs.set_title('TMB boxplot')
sns.boxplot(x,y,data=df)
plt.savefig('TMB.png',dpi=300)
