import math

#Total flow
Qtottmp = 5469
#UpHill level
Eamtmp = 172.110
NBstages=5
Sn = 5469 #the total number of allocated flow per turbine
track = [0]*NBstages


#H is the drop height
#def BuildingSolutionTree(H):
#Drop height computation
#Q turbined flow, i Stage(turbine)
def costFunction(Q,i):
    Q=Q/10
    H=computeDropHeight(Qtottmp/10,Eamtmp)
    if i==4:
        P = 0.08574 - 0.002519*H - 0.1976*Q + 0.008179*H*Q + 0.002893*Q*Q + 7.395 *math.pow(10,-6)  *H*Q*Q - 1.196 * math.pow(10,-5) *Q*Q*Q
    if i==3:
        P = 0.8117-0.02372*H -0.2443*Q+0.006487*H*Q+0.003843*Q*Q +2.211*math.pow(10,-5)*H*Q*Q -1.672 *math.pow(10,-5)*Q*Q*Q

    if i==2:
        P = -0.025 + 0.0009633*H - 0.2158*Q + 0.006349*H*Q + 0.003545*Q*Q + 2.217 *math.pow(10,-5) *H*Q*Q - 1.576 *math.pow(10,-5) *Q*Q*Q

    if i==1:
        P = -0.04626 + 0.001767*H - 0.1908*Q + 0.004949*H*Q + 0.003545*Q*Q + 3.488 *math.pow(10,-5) *H*Q*Q - 1.698 *math.pow(10,-5) *Q*Q*Q

    if i==0:
        P = 0.293-0.008025*H -0.1833*Q+0.008081*H*Q+0.002709*Q*Q +1.955*math.pow(10,-5)*H*Q*Q -1.325 *math.pow(10,-5)*Q*Q*Q

        
    return P

#Qtot total flow, Eam uphill level
def computeDropHeight(Qtot, Eam):
    return Eam-(-7.017 * math.pow(10,-7)*Qtot*Qtot + 0.004107 * Qtot + 137.2)

def StageN():
    track[NBstages-1]=[]
    for i in range(Sn+1):
        #print(costFunction(i,NBstages-1))
        track[NBstages-1].append([i,costFunction(i,NBstages-1),i])
    #print(track)
    return allStage(track,NBstages-1)

#track is the table of complete subproblems
def allStage(track, stage):
    print(stage)
    table=[0]*(math.ceil((Sn+1)))
    track[stage-1]=[]
    for i in range(Sn+1):

        table[i]=[]
        bestRank_Value = (0,0)
        for j in range(Sn+1):
            if(i>=j):
                #print(str(i)+" "+str(j))
                #print("f3* "+str(track[stage][i-j][1]))
                #print("F2* "+str(costFunction(j,stage-1)))
                #print(track[stage])
                value=track[stage][i-j][1]+costFunction(j,stage-1)
                table[i].append(value)
                if(value > bestRank_Value[1]):
                    bestRank_Value=(j,value)
            else:
                table[i].append(-1)
        track[stage-1].append([i,bestRank_Value[1],bestRank_Value[0]]) 
    #print(table)
    if(stage==1):
        return track
    else:
        return allStage(track, stage-1)

def computeFinalSolution(track):
    Solution=[]
    Cost=(track[0][Sn][1])
    Solution.append(track[0][(Sn-1)][2]/10)
    print(Solution[0])
    print(Cost)
    Ressources=Sn-track[0][(Sn-1)][2]
    for i in range(1,len(track)) :
        for j in track[i]:
            if j[0]==Ressources:
                Solution.append(j[2]/10)
                Ressources-=j[2]
                break
    return (Solution, Cost)
        
                    


print(computeFinalSolution(StageN()))
print(computeDropHeight(Qtottmp,Eamtmp))
