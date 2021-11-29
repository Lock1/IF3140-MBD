from operator import itemgetter

#Resource with default version=0, rts & wts =0
#X[i][0] = represent name of Resource, X[i][1] = represent version, X[i][2] = represent value, X[i][3] = represent rts, X[i][4] = represent wts
#u can add or edit resource
X=[["X",0,10,0,0]]
Y=[["Y",0,20,0,0]]

#Transaction with Timestamp 1 and 2
#Trn = Timestamp
#u can add or edit Timestamp
Tr1 = 1
Tr2 = 2

def read(a,b):
    if(len(b)==1):
        if(a>b[0][3]):
                b[0][3]=a
        print(f"Updated TS{b[0][0]} version{b[0][1]} = RTS:{b[0][3]} WTS:{b[0][4]}")

    else :
        #Mencari versi yang sesuai untuk dilakukan read
        for val in reversed(sorted(b, key=itemgetter(1))):
            if(a<val[4]):
                print(f"Looking for oldest version preventing rollback on TS{val[0]} version{val[1]} = RST:{val[3]} WTS:{val[4]}")
            else :
                if(a>val[3]):
                    val[3]=a
                print(f"Updated TS{val[0]} version{val[1]} = RST:{val[3]} WTS:{val[4]}")
                break

def write(a,b):
    if(len(b)==1):
        if(a>b[0][3]):
            b.append([b[0][0],a,b[0][2],a,a])
            print(f"Updated TS{b[0][0]} version{a} = RTS:{a} WTS:{a}")
        else :
            print("Rollback Transaction")
            return False
    else :
        #Mencari versi yang sesuai untuk dilakukan write
        for val in reversed(sorted(b, key=itemgetter(1))):
            if(a<val[4]):
                print(f"Looking for oldest version preventing rollback on TS{val[0]} version{val[1]} = RST:{val[3]} WTS:{val[4]}")
            else :
                if(a>val[3]):
                    b.append([val[0],a,val[2],a,a])
                    print(f"Updated TS{val[0]} version{a} = RTS:{a} WTS:{a}")
                else :
                    print("Rollback Transaction")
                    return False


#Example of some Schedule with format [operation, Timestamp, Resource], edit this Schedule if u want a different scenario
Schedule=[["r",Tr1,X],["w",Tr2,X],["w",Tr2,Y],["w",Tr1,Y]] 
#example for Schedule for Rollback scenario
#Schedule=[["r",Tr1,X],["w",Tr2,X],["w",Tr2,Y],["w",Tr1,Y]]
end=True
for transaction in Schedule:
    if(transaction[0]=="r"):
        read(transaction[1],transaction[2])
    else : #asumsi inputan pengguna benar
        if((write(transaction[1],transaction[2]))==False):
            end=False
            break
if(end) :
    print("Commited all Trasanction because no Rollback detected")
else :
    print("Failed to Commit Transaction because Rollback detected")
