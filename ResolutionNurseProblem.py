import math

#Total flow
Qtottmp = 548
#Upstream level
Eamtmp = 172
NBstages=3
Sn = 5 #the total number of allocated flow
track = [0]*NBstages
CalculationMatrix=[[0,0,0],
        [45,20,50],
    [70,45,70],
    [90,75,80],
    [105,110,100],
    [120,150,130]]

#H is the drop height
#def BuildingSolutionTree(H):
#Drop height computation

def costFunction(Xn,i):
    return CalculationMatrix[Xn][i]


def computeDropHeight(Qtot, Eam):
    return Eam-(-7.017 * math.pow(10,-7)*Qtot*Qtot + 0.004107 * Qtot + 137.2)

def StageN():
    track[NBstages-1]=[]
    for i in range(Sn+1):
        #print(costFunction(i,NBstages-1))
        track[NBstages-1].append([i,costFunction(i,NBstages-1),i])
    #print(track)
    return allStage(track,NBstages-1)

def allStage(track, stage):
    table=[0]*(Sn+1)
    track[stage-1]=[]
    for i in range(Sn+1):

        table[i]=[]
        bestRank_Value = (0,0)
        for j in range(Sn+1):
            if(i>=j):
                #print(str(i)+" "+str(j))
                #print("f3* "+str(track[stage][i-j][1]))
                #print("F2* "+str(costFunction(j,stage-1)))
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
    Solution.append(track[0][Sn-1][2])
    Ressources=Sn-Solution[0]
    for i in range(1,len(track)) :
        for j in track[i]:
            if j[0]==Ressources:
                Solution.append(j[2])
                Ressources-=j[2]
                break
    return (Solution, Cost)
        
                    


print(computeFinalSolution(StageN()))
print(computeDropHeight(Qtottmp,Eamtmp))
