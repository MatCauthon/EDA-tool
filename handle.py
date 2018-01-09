import numpy as np
import sys
from component import*
file_handle=open('/Users/feisigou/PycharmProjects/HW3/test_diode','r')

line=file_handle.readline()
line=line.strip().lower()

#strip() removes white spaces(including '\n','\r','\t')
line_elements=line.split()
line_num=0
net_num=-1
ctrl_num=-1
h=0 #.tran simualtion 's step and it should be larger than 0
TranTime=0 #.tran simualtion 's whole runtime
CurrentTranTime=0
CurrentTranNode=0
TranNode=0
PrintFlag=0 #set PrintFlag to 1 when command lines has a .print
TranFlag=0
print_cmd=[]
print_num=-1
comment=[]
element=[]
control=[]
elements=['r','c','v','i','h','g','f','e','d']
comment_line=[]
element_line=[]
control_line=[]
NetList=[]

RHS=[]

def get_time_value(char):
        units = {
            'k': 1e3,
            'm': 1e-3,
            'u': 1e-6,
            'n': 1e-9,
            'p': 1e-12,
            'f': 1e-15,
        }
        #print(char)
        if units.get(char[-2]):
            print(eval(char[:-2])*units[char[-2]])
            return eval(char[:-2])*units[char[-2]]
        else:
            return eval(char)

while line:

    line_num = line_num+1
    """if line[0] not in {'*','v','r','.'}:
        print("netlist error")
        break"""

    """#print the netlist
    if line_num==1:
        print("The netlist is shown below:")
    print(line)
    """
    if line_elements[0][0]== '*':

        comment_line.append(line_num)
    elif line_elements[0][0] in elements:

        element_line.append(line_num)
        # create a netlist with only element lines
        net_num += 1
        NetList.append(line_elements)

    elif line_elements[0][0]== '.':
        control.append(line_elements) # save details of control lines
        control_line.append(line_num) #get control lines' line num
        ctrl_num += 1
        if line_elements[0] == '.tran':
            print(control[ctrl_num])
            h=get_time_value(control[ctrl_num][1])
            print("h*10e9 in handle.py is:%f"%(h*10e9))
         #   print("h is calculated here value is: %fline78"%(h))
            TranTime=get_time_value(control[ctrl_num][2])
            print("TranTime is:%f"%(TranTime*10e8))
            if not ( h>0 and TranTime>0 ):
                print("parameters of .tran has an error")
            TranFlag = 1
            TranNode = TranTime/h
         #   print(TranNode,TranTime,h,'line84')


        if line_elements[0] == '.print':
            PrintFlag=1
            print_cmd.append(line_elements)

            print_num += 1




    #find out the components and make the MNA
   # if line[0]=='r':



    line=file_handle.readline()
    line=line.strip().lower()
    line_elements=line.split()


"""#show line details
print("\n")
print("*****************property of all lines are shown below****************")
print("total lines : %d"%line_num)
print("comment lines are:",end="")
print(comment_line)
print("element lines are:",end="")
print(element_line)
print("control lines are:",end="")
print(control_line)
"""

"""#print the netlist as a matrix
for i in range(0,net_num+1):
    print(NetList[i])"""








