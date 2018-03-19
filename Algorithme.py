import math

#Total flow
Qtottmp = 548
#Upstream level
Eamtmp = 172

#H is the drop height
#def BuildingSolutionTree(H):
#Drop height computation

def computeDropHeight(Qtot, Eam):
    return Eam-(-7.017 * math.pow(10,-7)*Qtot*Qtot + 0.004107 * Qtot + 137.2)

print(computeDropHeight(Qtottmp,Eamtmp))
