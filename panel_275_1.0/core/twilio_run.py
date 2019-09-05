from twilio.rest import Client
import sys

def run(project_name):
    accountSID="ACd271a2d8ea2b0973c7bbef3a876254dc"
    authToken="bebb72660229db0a481883228fde9e60"
    Twilio = '+17653990741'
    Phone="+8618621084524"
    client=Client(accountSID,authToken)
    client.messages.create(from_=Twilio,to=Phone,body="The process %s has done."%(project_name))

if __name__=="__main__":
    if len(sys.argv)!=2:
        print("python3 %s project_name"%(sys.argv[0]))
        print("#Email:fanyucai1@126.com")
    else:
        project_name=sys.argv[1]
        run(project_name)
