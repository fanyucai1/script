import pytablewriter
import fire

def convert(tab):
    writer = pytablewriter.RstGridTableWriter()
    writer.table_name = "table_rst"
    file=open(tab,"r")
    num=0
    mylist=[]
    for line in file:
        line=line.strip()
        temp=line.split("\t")
        mylist.append(temp)

    writer.value_matrix=mylist
    writer.write_table()


if __name__ =="__main__":
    fire.Fire()
