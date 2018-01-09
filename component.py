from math import *
import numpy as np
class component:
    def __init__(self,para):
        self.para=para
        self.get_para()

    def get_para(self):
        if len(self.para)<4:
            print("component error: there are no enough parameters")
            return
        self.name=self.para[0]
        self.pos1=eval(self.para[1])
        self.pos2=eval(self.para[2])
        self.para_value=self.para[3:]

    def get_value(self, char):
        units = {
            'k': 1e3,
            'm': 1e-3,
            'u': 1e-6,
            'n': 1e-9,
            'p': 1e-12,
            'f': 1e-15,
        }
        if units.get(char[-1]):
            return eval(char[:-1])*units[char[-1]]
        else:
            return eval(char)

    def max_pos(self):
        return max(self.pos1,self.pos2)

class Resistor(component):
    def __init__(self,*av):
        component.__init__(self,*av)
        # *av inherit para from component
        self.value=self.get_value(self.para_value[0])

class Capacitor(component):
    def __init__(self,*av):
        component.__init__(self,*av)
        # *av inherit para from component
        self.value=self.get_value(self.para_value[0])

class Inductor(component):
    def __init__(self,*av):
        component.__init__(self,*av)
        # *av inherit para from component
        self.value=self.get_value(self.para_value[0])


class CurrentSource(component):
    def __init__(self,*av):
        component.__init__(self,*av)
        # *av inherit para from component
        self.value=self.get_value(self.para_value[0])

class VoltageSource(component):
    def __init__(self,*av):
        component.__init__(self,*av)
        # *av inherit para from component
        self.value=self.get_value(self.para_value[0])

class VCVS(component):
    def __init__(self,*av):
        component.__init__(self,*av)
        # *av inherit para from component
        self.Getvalue()

    def Getvalue(self):
        if len(self.para_value)<3:
            print("num of parameters error for VCVS")
            return
        self.pos3=eval(self.para_value[0])
        self.pos4=eval(self.para_value[1])
        self.value=self.get_value(self.para_value[2])

class CCCS(component):
    def __init__(self,*av):
        component.__init__(self,*av)
        # *av inherit para from component
        self.Getvalue()

    def Getvalue(self):
        if len(self.para_value)<3:
            print("num of parameters error for CCCS")
            return
        self.vname=self.para_value[0]
        self.value=self.get_value(self.para_value[1])


class VCCS(component):
    def __init__(self,*av):
        component.__init__(self,*av)
        # *av inherit para from component
        self.Getvalue()

    def Getvalue(self):
        if len(self.para_value)<3:
            print("num of parameters error for VCCS")
            return
        self.pos3=eval(self.para_value[0])
        self.pos4=eval(self.para_value[1])
        self.value=self.get_value(self.para_value[2])

class CCVS(component):
    def __init__(self,*av):
        component.__init__(self,*av)
        # *av inherit para from component
        self.Getvalue()

    def Getvalue(self):
        if len(self.para_value)<3:
            print("num of parameters error for CCVS")
            return
        self.vname=self.para_value[0]

        self.value=self.get_value(self.para_value[1])

class diode(component):
    def __init__(self,*av):
        component.__init__(self,*av)
        self.Getvalue()

    def Getvalue(self):
        self.alpha=40
        self.Isat=1
        self.VI=0
        self.VI_last=0
        #self.Isat=10e-15
        # Id=Isat*(exp(self.alpha*Vd)-1)

    def Gn(self, vd):
        #print ("gn is %f"%(self.Isat*self.alpha*exp(self.alpha*vd)))
        return self.Isat*self.alpha*exp(self.alpha*vd)

    def In(self, vd):
        #print 'in', -Isat*self.aplha*exp(self.aplha*vd)*vd+Isat*(exp(self.aplha*vd)-1)
        return -self.Isat*self.alpha*exp(self.alpha*vd)*vd+self.Isat*(exp(self.alpha*vd)-1)

    def convergence(self):
        c1 = 1e-6
        c2 = 1e-4
        if abs(self.VI - self.VI_last) <= min(c1, c2*abs(self.VI_last)):
            return 1
        else:
            return 0


