import math
import sys

#Total flow
#Qtottmp = 548
#UpHill level
#Eamtmp = 172.110
NBstages=6
Sn = [180,180,180,180,180,180] #the total number of allocated flow per turbine
track = [0]*NBstages


#H is the drop height
#def BuildingSolutionTree(H):
#Drop height computation
#Q turbined flow, i Stage(turbine)
def costFunction(Q,i,Qtot,Eam ):
    Q=Q
    H=computeDropHeight(Qtot,Eam)
    #pertes = 0.5*math.exp(-5)*Q*Q
    if (Q==0):
        return 0
    if i==1:
        P = 0.08574 - 0.002519*H - 0.1976*Q + 0.008179*H*Q + 0.002893*Q*Q + 7.395 *math.pow(10,-6)  *H*Q*Q - 1.196 * math.pow(10,-5) *Q*Q*Q
    
    if i==2:
        P = 0.8117-0.02372*H -0.2443*Q+0.006487*H*Q+0.003843*Q*Q +2.211*math.pow(10,-5)*H*Q*Q -1.672 *math.pow(10,-5)*Q*Q*Q

    if i==3:
        P = -0.025 + 0.0009633*H - 0.2158*Q + 0.006349*H*Q + 0.003545*Q*Q + 2.217 *math.pow(10,-5) *H*Q*Q - 1.576 *math.pow(10,-5) *Q*Q*Q

    if i==4:
        P = -0.04626 + 0.001767*H - 0.1908*Q + 0.004949*H*Q + 0.003545*Q*Q + 3.488 *math.pow(10,-5) *H*Q*Q - 1.698 *math.pow(10,-5) *Q*Q*Q

    if i==5:
        P = 0.293-0.008025*H -0.1833*Q+0.008081*H*Q+0.002709*Q*Q +1.955*math.pow(10,-5)*H*Q*Q -1.325 *math.pow(10,-5)*Q*Q*Q

        
    return P

#Qtot total flow, Eam uphill level
def computeDropHeight(Qtot, Eam):
    return Eam-(-7.017 * math.pow(10,-7)*Qtot*Qtot + 0.004107 * Qtot + 137.2)
    #return 0.002989 * Qtot +137.6
    
if __name__ == "__main__":
    H=172.12
    Qtot=540
    Ptot=0
    
    for i in range(1,len(sys.argv)) : 
        Ptot+=costFunction(int(sys.argv[i]),i,Qtot,H)
    print(Ptot)
        
    
    
    

#launchAlgorithme(813,172.192)
#launchAlgorithme()
#print(computeDropHeight(Qtottmp,Eamtmp))
