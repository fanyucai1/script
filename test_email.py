import poplib
M=poplib.POP3("pop.126.com")
M.user("fanyucai1")
M.pass_("fyc840924")
numMessages = len(M.list()[1])
for i in range(numMessages):
    for j in M.retr(i+1)[1]:
        print(j)