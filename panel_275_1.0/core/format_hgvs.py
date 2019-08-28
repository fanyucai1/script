import sys
import re

def run(var_site):
    p1=re.search(r'[A-Z]fs\*\d+$',var_site)###匹配移码突变
    p2=re.search(r'del([ACGT]+)ins',var_site)###匹配del和ins
    if p1:
        new=re.sub(r'[A-Z]fs\*\d+$',"",var_site)
        new=new+"fs"
    else:
        new=var_site
    if var_site.endswith("X"):####终止密码子X替换*
        new1= re.sub(r'X$', "*", new)
    else:
        new1=new
    if p2:
        new2=re.sub(p2.group(1),"",new1,count=1)
    else:
        new2 = new1
    print(new2)


if __name__=="__main__":
    if len(sys.argv)!=2:
        print("usage:python3 %s var_site" %(sys.argv[0]))
        print("#Email:fanyucai1@126.com")
    else:
        var_site=sys.argv[1]
        run(var_site)