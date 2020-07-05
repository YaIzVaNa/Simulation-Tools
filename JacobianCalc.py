# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 18:24:04 2019

@author: yaelb
"""

from pyomo.environ import * 
from pyomo.core.base.symbolic import differentiate 
from pyomo.dae import * 
###This import changes
from pyomo.core.expr import current as EXPR

m = ConcreteModel()

#Unindexed vars
m.x = Var() 
m.y = Var()
m.z = Var()
m.idx=RangeSet(1,3)

#indexed vars
m.t=ContinuousSet(bounds=(0,2))
m.x_idx=Var(m.idx,m.t)
m.y_idx=Var(m.idx,m.t)
m.z_idx=Var(m.idx,m.t)

#Objective function
m.Obj = Objective(expr = m.y*m.x**3 + m.y**2)

#Simple constraint
m.c1=Constraint(expr= m.x**2+m.y**2+m.x*m.y+m.z==0)

#Indexed constraint
def idxCons(m,i):
    if i==1:
        return m.x*m.y==8
    if i==2:
        return m.y*m.z==8
    if i==3:
        return m.z*m.x*m.y==8
m.c2=Constraint(m.idx,rule=idxCons)

def idxConsidxVar(m,i,t):
#    if(i==1):
        return m.x_idx[i,t]*m.y_idx[i,t]*m.z_idx[i,t]==0
#    if(i==2):
#        return m.y_idx[i,t]*m.z_idx[i,t]**2==0
#    if(i==3):
#        return m.x_idx[i,t]*m.z_idx[i,t]**2==0
m.c3=Constraint(m.idx,m.t,rule=idxConsidxVar)

def idxConsidxVar(m,i,t):
    return m.x_idx[i,t]**2==0
m.c4=Constraint(m.idx,m.t,rule=idxConsidxVar)


#discretizer = TransformationFactory('dae.collocation')
#discretizer.apply_to(m, nfe=8, ncp=4)

### To obtain derivatives wrt Objective function
print("Jacobian of Objective function:")
varList = list(EXPR.identify_variables(m.Obj.expr) )
FrstDerivs = differentiate(m.Obj.expr, wrt_list=varList)
[print('    derivative wrt',varList[idx],':',item) for idx, item in enumerate(FrstDerivs)]

### To obtain derivatives wrt Constraint 1, a simple un-indexed constraint
print("Jacobian of c1 (Simple constraint):")
varList = list(EXPR.identify_variables(m.c1.body) )
FrstDerivs = differentiate(m.c1.body, wrt_list=varList)
[print('    derivative wrt',varList[idx],':',item) for idx, item in enumerate(FrstDerivs)]

### To obtain derivatives wrt Constraint 2, an indexed constraint
print("Jacobian of c2 (indexed constraint):")
varList=[[] for i in m.c2]
FrstDerivs=[[] for i in m.c2]
for i in m.c2:
    varList[i-1]=list(EXPR.identify_variables(m.c2[i].body))
for i in m.c2:
    FrstDerivs[i-1] = differentiate(m.c2[i].body, wrt_list=varList[i-1])
for i in m.c2:
    [print('    index',i,', derivative wrt',varList[i-1][idx],':',item) for idx, item in enumerate(FrstDerivs[i-1])]

### To obtain derivatives wrt Constraint 3, an indexed constraint with indexed variables
print("Jacobian of c3 (indexed constraint, indexed variables):")
varList3=[[] for idx,i in enumerate(m.c3)]
FrstDerivs3=[[] for idx,i in enumerate(m.c3)]
for idx,i in enumerate(m.c3):
    varList3[idx-1]=list(EXPR.identify_variables(m.c3[i].body))
for idx,i in enumerate(m.c3):
    FrstDerivs3[idx-1] = differentiate(m.c3[i].body, wrt_list=varList3[idx-1])
#for idx,i in enumerate(m.c3):
#    [print('    index',idx,', derivative wrt',varList[idx-1][idx2],':',item) for idx2, item in enumerate(FrstDerivs[idx-1])]
[print('    index',0,', derivative wrt',varList3[0][idx2],':',item) for idx2, item in enumerate(FrstDerivs3[0])]

print("Jacobian of c4 (indexed constraint, indexed variables):")
varList=[[] for idx,i in enumerate(m.c4)]
FrstDerivs=[[] for idx,i in enumerate(m.c4)]
for idx,i in enumerate(m.c4):
    varList[idx-1]=list(EXPR.identify_variables(m.c4[i].body))
for idx,i in enumerate(m.c4):
    FrstDerivs[idx-1] = differentiate(m.c4[i].body, wrt_list=varList3[idx-1])
#for idx,i in enumerate(m.c3):
#    [print('    index',idx,', derivative wrt',varList[idx-1][idx2],':',item) for idx2, item in enumerate(FrstDerivs[idx-1])]
[print('    index',0,', derivative wrt',varList3[0][idx2],':',item) for idx2, item in enumerate(FrstDerivs[0])]

