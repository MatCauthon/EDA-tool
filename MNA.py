from handle import*
import matplotlib.pyplot as plt
# dc simulation
CCVname=[] #save CC names
CCStampFlag=[] # used to get whether a CC is stamped(as a CC should only be stamped once)
CCRows=[]
InductorList={} #used to get the exact row in MNA influenced by an Inductor
CapacitorList={}
CapacitorV=[]
CapacitorI={}
V2=[]
Time=[]
max_node=-1
rows=0
NodeX=[]
NodeX_all=[]
PrintNode=0
PrintOutY=[]
NonLinearFlag=0
NonLinearList=[]
MNA_all=[]
RHS_all=[]
# MNA_all = MNA + MNA_nl
# MNA is MNA stamp for linear equipments
# MNA_nl is MNA stamp for nonlinear equipments
# MNA_all is the whole MNA stamp for all equipments
VIList=[]
fv=[]

for i in range(0,net_num+1):
    #print(NetList[i])
    tmp=component(NetList[i])
    max_node=max(max_node,tmp.max_pos())
    rows=max_node+1
    MNA = np.zeros((rows, rows))
    RHS = np.zeros(rows)
    MNA_nl = np.zeros((rows,rows))
    RHS_nl = np.zeros(rows)
for i in range(0,net_num+1):
    if NetList[i][0][0]=='r':
        tmp=Resistor(NetList[i])
        MNA[tmp.pos1, tmp.pos1] += 1./tmp.value
        MNA[tmp.pos1, tmp.pos2] -= 1./tmp.value
        MNA[tmp.pos2, tmp.pos1] -= 1./tmp.value
        MNA[tmp.pos2, tmp.pos2] += 1./tmp.value
    if NetList[i][0][0]=='c':
        print("Capacitor behave as nothing in .dc simulation")
        CapacitorI[NetList[i][0]]=0
    if NetList[i][0][0]=='l':
        tmp=VoltageSource(NetList[i][0],NetList[i][1],NetList[i][2],0)
        MNA = np.column_stack((MNA, np.zeros(rows)))
        MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
        rows += 1
        MNA = np.row_stack((MNA, np.zeros(rows)))
        MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
        RHS = np.append(RHS, np.zeros(1))
        RHS_nl = np.append(RHS_nl, np.zeros(1))
        MNA[tmp.pos1, rows-1] += 1
        MNA[tmp.pos2, rows-1] -= 1
        MNA[rows-1, tmp.pos1] += 1
        MNA[rows-1, tmp.pos2] -= 1
        RHS[rows-1] = tmp.value
        #InductorNum += 1
        InductorList[NetList[i][0]]=rows

    if NetList[i][0][0]=='i':
        tmp=CurrentSource(NetList[i])
        RHS[tmp.pos1] -= 1./tmp.value
        RHS[tmp.pos2] += 1./tmp.value
    if NetList[i][0][0]=='v':
        tmp=VoltageSource(NetList[i]) # it is possible that tmp is a part of CCVS or CCCS
        if NetList[i][0][0] not in CCVname:

            MNA = np.column_stack((MNA, np.zeros(rows)))
            MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
            rows += 1
            MNA = np.row_stack((MNA, np.zeros(rows)))
            MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
            RHS = np.append(RHS, np.zeros(1))
            RHS_nl = np.append(RHS_nl, np.zeros(1))
            MNA[tmp.pos1, rows-1] += 1
            MNA[tmp.pos2, rows-1] -= 1
            MNA[rows-1, tmp.pos1] += 1
            MNA[rows-1, tmp.pos2] -= 1
            RHS[rows-1] = tmp.value
        else:

            j=0
            while CCVname[j][3]!= NetList[i][0][0]:
                j += 1
            #CCVS(H)
            if CCVname[j][0][0] == 'h':

                if CCStampFlag[j] == 0:
                    CCStampFlag[j] += 1
                    MNA = np.column_stack((MNA, np.zeros(rows)))
                    MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
                    rows += 1
                    MNA = np.row_stack((MNA, np.zeros(rows)))
                    MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
                    RHS = np.append(RHS, np.zeros(1))
                    RHS_nl = np.append(RHS_nl, np.zeros(1))
                    MNA[rows-1, tmp.pos1] += 1
                    MNA[rows-1, tmp.pos2] -= 1
                    MNA[tmp.pos1, rows-1] += 1
                    MNA[tmp.pos2, rows-1] -= 1
                    MNA[CCRows[j], rows-1] -= CCVname[j][4]
                    RHS[rows-1] = tmp.value
                elif CCStampFlag[j] == 1:
                    MNA = np.column_stack((MNA, np.zeros(rows)))
                    MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
                    rows += 1
                    MNA = np.row_stack((MNA, np.zeros(rows)))
                    MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
                    RHS = np.append(RHS, np.zeros(1))
                    RHS_nl = np.append(RHS_nl, np.zeros(1))
                    MNA[CCRows[j], rows-1] -= CCVname[j][4]

            elif CCVname[j][0][0] == 'f':
                if CCStampFlag[j] == 0:

                    CCStampFlag[j] += 1
                    MNA = np.column_stack((MNA, np.zeros(rows)))
                    MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
                    rows += 1
                    MNA = np.row_stack((MNA, np.zeros(rows)))
                    MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
                    RHS = np.append(RHS, np.zeros(1))
                    RHS_nl = np.append(RHS_nl, np.zeros(1))
                    MNA[CCVname[j][1], rows-1] += CCVname[j][4]
                    MNA[CCVname[j][2], rows-1] -= CCVname[j][4]
                    MNA[tmp.pos1, rows-1] += 1
                    MNA[tmp.pos2, rows-1] -= 1
                    MNA[rows-1, tmp.pos1] += 1
                    MNA[rows-1, tmp.pos2] -= 1
                    RHS[rows-1] = tmp.value
                elif CCStampFlag[j] == 1:
                    MNA = np.column_stack((MNA, np.zeros(rows)))
                    MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
                    rows += 1
                    MNA = np.row_stack((MNA, np.zeros(rows)))
                    MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
                    RHS = np.append(RHS, np.zeros(1))
                    RHS_nl = np.append(RHS_nl, np.zeros(1))
                    MNA[CCVname[j][1], rows-1] += CCVname[j][4]
                    MNA[CCVname[j][2], rows-1] -= CCVname[j][4]

    if NetList[i][0][0]=='h':
        tmp=CCVS(NetList[i])
        MNA = np.column_stack((MNA, np.zeros(rows)))
        MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
        rows += 1
        MNA = np.row_stack((MNA, np.zeros(rows)))
        MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
        RHS = np.append(RHS, np.zeros(1))
        RHS_nl = np.append(RHS_nl, np.zeros(1))

        MNA[tmp.pos1, rows-1] += 1
        MNA[tmp.pos2, rows-1] -= 1
        MNA[rows-1, tmp.pos1] += 1
        MNA[rows-1, tmp.pos2] -= 1
        CCVname.append(tmp)
        CCStampFlag.append(0)
        CCRows.append(rows)

    if NetList[i][0][0] == 'f':
        tmp=CCCS(NetList[i])
        CCVname.append(tmp)
        CCStampFlag.append(0)
        CCRows.append(rows)


    if NetList[i][0][0]=='g':
        tmp=VCCS(NetList[i])
        MNA[tmp.pos1, tmp.pos3] += tmp.value
        MNA[tmp.pos1, tmp.pos4] -= tmp.value
        MNA[tmp.pos2, tmp.pos3] -= tmp.value
        MNA[tmp.pos2, tmp.pos4] += tmp.value

    if NetList[i][0][0]=='e':
        tmp=VCVS(NetList[i])
        MNA = np.column_stack((MNA, np.zeros(rows)))
        MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
        rows += 1
        MNA = np.row_stack((MNA, np.zeros(rows)))
        MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))

        MNA[tmp.pos1, rows-1] += 1
        MNA[tmp.pos2, rows-1] -= 1
        MNA[rows-1, tmp.pos1] += 1
        MNA[rows-1, tmp.pos2] -= 1
        MNA[rows-1, tmp.pos3] -= tmp.value
        MNA[rows-1, tmp.pos4] += tmp.value








#print("*********************  MNA of .dc simulation is shown below:  ***********************")
#print(MNA)
#print("*********************  RHS of .dc simulation is shown below:  ***********************")

#print(RHS)

# NodeX is the solution of MNA*NodeX=RHS
NodeX=np.append(np.zeros(1),np.linalg.solve(MNA[1:,1:],RHS[1:]))
#print("*********************   NodeX of .dc simulation is shown below: *********************")
#print(NodeX)
"""print(type(PrintNode))
print(NodeX)
print(PrintNode)
PrintOutY.append(NodeX[2])
Time.append(CurrentTranTime)"""



if TranFlag :  # .tran simulation
    #print("*************this is before the while")
    if PrintFlag:
        if print_cmd[0][1] == 'tran':
            if print_cmd[0][2][0] == 'v':
                PrintNode += 0

                PrintNode += eval(print_cmd[0][2][2])
                PrintNode=int(PrintNode)
        print("PrintNode is %d"%(PrintNode))
    while CurrentTranTime < TranTime :
        #print("*********** CurrentTranTime is %f and TranTime is %f"%(CurrentTranTime,TranTime))
        CurrentTranTime += h
        #print("h is: %f"%(h))
        #print("CurrentTranTime*10e8 is : %f"%(CurrentTranTime*10e8))
        CurrentTranNode += 1
        if CurrentTranTime == TranTime:
            print("CurrentTranTime==TranTime")
        CCVname=[] #save CC names
        CCStampFlag=[] # used to get whether a CC is stamped(as a CC should only be stamped once)
        CCRows=[]
        max_node=-1
        rows=0
        for i in range(0,net_num+1):
            #print(NetList[i])
            tmp=component(NetList[i])
            max_node=max(max_node,tmp.max_pos())
            rows=max_node+1
            MNA = np.zeros((rows, rows))
            MNA_nl = np.zeros((rows, rows))
            RHS = np.zeros(rows)
            RHS_nl = np.zeros(rows)

        for i in range(0,net_num+1):
            if NetList[i][0][0]=='r':
                tmp=Resistor(NetList[i])
                MNA[tmp.pos1, tmp.pos1] += 1./tmp.value
                MNA[tmp.pos1, tmp.pos2] -= 1./tmp.value
                MNA[tmp.pos2, tmp.pos1] -= 1./tmp.value
                MNA[tmp.pos2, tmp.pos2] += 1./tmp.value
            if NetList[i][0][0]=='c':
                tmp=Capacitor(NetList[i])

                MNA = np.column_stack((MNA, np.zeros(rows)))
                MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
                rows += 1
                CapacitorList[NetList[i][0]]=rows
                MNA = np.row_stack((MNA, np.zeros(rows)))
                MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
                RHS = np.append(RHS, np.zeros(1))
                RHS_nl = np.append(RHS_nl, np.zeros(1))
                MNA[tmp.pos1, rows-1] += 1
                MNA[tmp.pos2, rows-1] -= 1
                MNA[rows-1, tmp.pos1] += 2*tmp.value/h
                MNA[rows-1, tmp.pos2] -= 2*tmp.value/h
                MNA[rows-1, rows-1] -= 1
                #this NodeX is h time before CurrentTranTime as NodeX[t-h]
                #if CurrentTranTime > h :

                RHS[rows-1] += (2*tmp.value*(NodeX[tmp.pos1]-NodeX[tmp.pos2])/h + CapacitorI[NetList[i][0]])
                #elif CurrentTranTime == h:
                #    RHS[rows-1] += 2*tmp.value*(NodeX[tmp.pos1-1]-NodeX[tmp.pos2-1])

            if NetList[i][0][0]=='l':
                tmp=Inductor(NetList[i])
                MNA = np.column_stack((MNA, np.zeros(rows)))
                MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
                rows += 1
                MNA = np.row_stack((MNA, np.zeros(rows)))
                MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
                RHS = np.append(RHS, np.zeros(1))
                RHS_nl = np.append(RHS_nl, np.zeros(1))
                MNA[tmp.pos1, rows-1] += 1
                MNA[tmp.pos2, rows-1] -= 1
                MNA[rows-1, tmp.pos1] += 1
                MNA[rows-1, tmp.pos2] -= 1
                MNA[rows-1, rows-1] -= 2*tmp.value/h
                RHS[rows-1] += (-(NodeX[tmp.pos1]-NodeX[tmp.pos2])+2*tmp.value*NodeX[InductorList[NetList[i][0]]-1] )


            if NetList[i][0][0]=='i':
                tmp=CurrentSource(NetList[i])
                RHS[tmp.pos1] -= tmp.value
                RHS[tmp.pos2] += tmp.value
            if NetList[i][0][0]=='v':
                tmp=VoltageSource(NetList[i]) # it is possible that tmp is a part of CCVS or CCCS
                if NetList[i][0][0] not in CCVname:

                    MNA = np.column_stack((MNA, np.zeros(rows)))
                    MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
                    rows += 1
                    MNA = np.row_stack((MNA, np.zeros(rows)))
                    MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
                    RHS = np.append(RHS, np.zeros(1))
                    RHS_nl = np.append(RHS_nl, np.zeros(1))
                    MNA[tmp.pos1, rows-1] += 1
                    MNA[tmp.pos2, rows-1] -= 1
                    MNA[rows-1, tmp.pos1] += 1
                    MNA[rows-1, tmp.pos2] -= 1
                    RHS[rows-1] = tmp.value
                else:

                    j=0
                    while CCVname[j][3]!= NetList[i][0][0]:
                        j += 1
                    #CCVS(H)
                    if CCVname[j][0][0] == 'h':

                        if CCStampFlag[j] == 0:
                            CCStampFlag[j] += 1
                            MNA = np.column_stack((MNA, np.zeros(rows)))
                            MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
                            rows += 1
                            MNA = np.row_stack((MNA, np.zeros(rows)))
                            MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
                            RHS = np.append(RHS, np.zeros(1))
                            RHS_nl = np.append(RHS_nl, np.zeros(1))
                            MNA[rows-1, tmp.pos1] += 1
                            MNA[rows-1, tmp.pos2] -= 1
                            MNA[tmp.pos1, rows-1] += 1
                            MNA[tmp.pos2, rows-1] -= 1
                            MNA[CCRows[j], rows-1] -= CCVname[j][4]
                            RHS[rows-1] = tmp.value
                        elif CCStampFlag[j] == 1:
                            MNA = np.column_stack((MNA, np.zeros(rows)))
                            MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
                            rows += 1
                            MNA = np.row_stack((MNA, np.zeros(rows)))
                            MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
                            RHS = np.append(RHS, np.zeros(1))
                            RHS_nl = np.append(RHS_nl, np.zeros(1))
                            MNA[CCRows[j], rows-1] -= CCVname[j][4]

                    elif CCVname[j][0][0] == 'f':
                        if CCStampFlag[j] == 0:

                            CCStampFlag[j] += 1
                            MNA = np.column_stack((MNA, np.zeros(rows)))
                            MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
                            rows += 1
                            MNA = np.row_stack((MNA, np.zeros(rows)))
                            MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
                            RHS = np.append(RHS, np.zeros(1))
                            RHS_nl = np.append(RHS_nl, np.zeros(1))
                            MNA[CCVname[j][1], rows-1] += CCVname[j][4]
                            MNA[CCVname[j][2], rows-1] -= CCVname[j][4]
                            MNA[tmp.pos1, rows-1] += 1
                            MNA[tmp.pos2, rows-1] -= 1
                            MNA[rows-1, tmp.pos1] += 1
                            MNA[rows-1, tmp.pos2] -= 1
                            RHS[rows-1] = tmp.value
                        elif CCStampFlag[j] == 1:
                            MNA = np.column_stack((MNA, np.zeros(rows)))
                            MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
                            rows += 1
                            MNA = np.row_stack((MNA, np.zeros(rows)))
                            MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
                            RHS = np.append(RHS, np.zeros(1))
                            RHS_nl = np.append(RHS_nl, np.zeros(1))
                            MNA[CCVname[j][1], rows-1] += CCVname[j][4]
                            MNA[CCVname[j][2], rows-1] -= CCVname[j][4]

            if NetList[i][0][0]=='h':
                tmp=CCVS(NetList[i])
                MNA = np.column_stack((MNA, np.zeros(rows)))
                MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
                rows += 1
                MNA = np.row_stack((MNA, np.zeros(rows)))
                MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))
                RHS = np.append(RHS, np.zeros(1))
                RHS_nl = np.append(RHS_nl, np.zeros(1))

                MNA[tmp.pos1, rows-1] += 1
                MNA[tmp.pos2, rows-1] -= 1
                MNA[rows-1, tmp.pos1] += 1
                MNA[rows-1, tmp.pos2] -= 1
                CCVname.append(tmp)
                CCStampFlag.append(0)
                CCRows.append(rows)

            if NetList[i][0][0] == 'f':
                tmp=CCCS(NetList[i])
                CCVname.append(tmp)
                CCStampFlag.append(0)
                CCRows.append(rows)


            if NetList[i][0][0]=='g':
                tmp=VCCS(NetList[i])
                MNA[tmp.pos1, tmp.pos3] += tmp.value
                MNA[tmp.pos1, tmp.pos4] -= tmp.value
                MNA[tmp.pos2, tmp.pos3] -= tmp.value
                MNA[tmp.pos2, tmp.pos4] += tmp.value

            if NetList[i][0][0]=='e':
                tmp=VCVS(NetList[i])
                MNA = np.column_stack((MNA, np.zeros(rows)))
                MNA_nl = np.column_stack((MNA_nl, np.zeros(rows)))
                rows += 1
                MNA = np.row_stack((MNA, np.zeros(rows)))
                MNA_nl = np.row_stack((MNA_nl, np.zeros(rows)))

                MNA[tmp.pos1, rows-1] += 1
                MNA[tmp.pos2, rows-1] -= 1
                MNA[rows-1, tmp.pos1] += 1
                MNA[rows-1, tmp.pos2] -= 1
                MNA[rows-1, tmp.pos3] -= tmp.value
                MNA[rows-1, tmp.pos4] += tmp.value

            if NetList[i][0][0] == 'd':
              #  print("this is a diode")
                tmp=diode(NetList[i])
                NonLinearList.append(tmp)
                NonLinearFlag += 1
                MNA_nl[tmp.pos1, tmp.pos1] += tmp.Gn(0.1)
                MNA_nl[tmp.pos1, tmp.pos2] -= tmp.Gn(0.1)
                MNA_nl[tmp.pos2, tmp.pos1] -= tmp.Gn(0.1)
                MNA_nl[tmp.pos2, tmp.pos2] += tmp.Gn(0.1)
              #  print("tmp.In(0.1) is: %f"%(tmp.In(0.1)))
                RHS_nl[tmp.pos1] -= tmp.In(0.1)
                RHS_nl[tmp.pos2] += tmp.In(0.1)
              #  print("diode inital done")


        if NonLinearFlag > 0 :
           # print("NonLinearFlag>0")
            time=0
            MNA_all = MNA + MNA_nl
              #  print(MNA_all)
            RHS_all = RHS + RHS_nl
              #  print(RHS_all)
            NodeX_all=np.append(np.zeros(1),np.linalg.solve(MNA_all[1:,1:],RHS_all[1:]))
            print("NodeX_all is:")
            print(NodeX_all)
            VIList.append(0.1)
            fv.append(2*0.1/3 - 5/3 + exp(40*0.1))
            print("when VI==0.11:")
            print(2*0.11/3 - 5/3 + exp(40*0.11))
            while 1:

                flag=1

                MNA_nl=np.zeros((rows,rows))
                RHS_nl=np.zeros(rows)
                for i in range(len(NonLinearList)):

                    if NonLinearList[i].name[0] == 'd':
                      #  print("diode iteration")
                        tmp=NonLinearList[i]
                       # print("pos1 and pos2 : %d,%d"%(tmp.pos1,tmp.pos2))
                       # print("two pos V: %f,%f"%(NodeX_all[tmp.pos1],NodeX_all[tmp.pos2]))
                        tmp.VI_last = NodeX_all[tmp.pos1] - NodeX_all[tmp.pos2]
                       # print("VI_last is %f"%(tmp.VI_last))
                       # print(tmp.Gn(tmp.VI_last))
                        MNA_nl[tmp.pos1, tmp.pos1] += tmp.Gn(tmp.VI_last)
                        MNA_nl[tmp.pos1, tmp.pos2] -= tmp.Gn(tmp.VI_last)
                        MNA_nl[tmp.pos2, tmp.pos1] -= tmp.Gn(tmp.VI_last)
                        MNA_nl[tmp.pos2, tmp.pos2] += tmp.Gn(tmp.VI_last)
                        RHS_nl[tmp.pos1] -= tmp.In(tmp.VI_last)
                        RHS_nl[tmp.pos2] += tmp.In(tmp.VI_last)

                MNA_all = MNA + MNA_nl
                RHS_all = RHS + RHS_nl
                NodeX_all=np.append(np.zeros(1),np.linalg.solve(MNA_all[1:,1:],RHS_all[1:]))
                print("NodeX_all is:")
                print(NodeX_all)
                for i in range(len(NonLinearList)):
                    if NonLinearList[i].name[0] == 'd':
                        tmp=NonLinearList[i]
                        tmp.VI = NodeX_all[tmp.pos1] - NodeX_all[tmp.pos2]
                        print("tmp.VI and tmp.VI_last is:%f,%f"%(tmp.VI,tmp.VI_last))
                        VIList.append(tmp.VI)
                        print("fv is : ")
                        print(2*tmp.VI/3 - 5/3 + exp(40*tmp.VI))
                        fv.append(2*tmp.VI/3 - 5/3 + exp(40*tmp.VI))
                for i in range(len(NonLinearList)):
                    flag *= NonLinearList[i].convergence()
                 #   print("flag==%d"%(flag))
                if flag :
                    time=0
                    break
                time += 1
                #print("time== %d"%(time))
                if time >=3000 :
                    time=0
                    break
            print(VIList)
            #plt.plot(VIList,fv)
            x = np.linspace(0, 0.11, 100)
            plt.plot(x, 0.5*x-3./2+np.exp(40*x))
            for i in range(len(VIList)):
                plt.plot(x, (0.5+40*np.exp(40*VIList[i]))*(x-VIList[i])+0.5*VIList[i]-3./2+np.exp(40*VIList[i]),'--')
            plt.ylim(0,90)
            plt.show()
            break
            PrintNode=int(PrintNode)
            #print("Line 475 PrintNode is %d"%(PrintNode))
            #PrintOutY.append(NodeX_all[PrintNode])
            Time.append(CurrentTranTime)







        #print("********** CurrentTranTime is %f"%(CurrentTranTime))
        #print("****** CurrentTranNode is %fs from %f"%(CurrentTranNode,TranNode))
        #print("*********************  MNA  is shown below:  ***********************")
        #print(MNA)
        #print("*********************  RHS  is shown below:  ***********************")

        #print(RHS)
        #print("*********************  NodeX is shown below:  ***********************")
        #NodeX=np.append(np.zeros(1),np.linalg.solve(MNA[1:,1:],RHS[1:]))
        #print(NodeX)
        #print(int(PrintNode)
        #PrintNode=int(PrintNode)
        #print(type(PrintNode))
        #PrintOutY.append(NodeX_all[PrintNode])
        #Time.append(CurrentTranTime)


#plt.plot(Time,PrintOutY)
#plt.show()



