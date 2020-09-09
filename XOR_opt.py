# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 17:32:09 2020

@author: yaelb
"""
from pyomo.environ import *
from pyomo.dae import * 
from pyomo.opt import SolverFactory
import numpy as np


m= ConcreteModel()
m.xdim=RangeSet(1,2)
m.Xdim=RangeSet(1,4)

m.w = Var(m.xdim,initialize=1)
m.b = Var(bounds=(-5000,5000),initialize=0)
m.X = Param(m.Xdim, initialize={1:0,2:1,3:1,4:0})
m.x1 = Param(m.Xdim, initialize={1:0,2:1,3:0,4:1})
m.x2 = Param(m.Xdim, initialize={1:0,2:0,3:1,4:1})

m.Obj=Objective(sense=1,expr=sum((m.X[i]-((m.w[1]*m.x1[i])+m.w[2]*(m.x2[i])+m.b))**2 for i in m.Xdim))

SolverFactory('ipopt').solve(m).write()
