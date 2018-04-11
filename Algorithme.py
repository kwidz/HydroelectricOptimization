import math

#Total flow
#Qtottmp = 548
#UpHill level
#Eamtmp = 172.110
NBstages=6
Sn = [180,180,180,180,180,180] #the total number of allocated flow per turbine
track = [0]*NBstages
discret5 = False

#H is the drop height
#def BuildingSolutionTree(H):
#Drop height computation
#Q turbined flow, i Stage(turbine)
def costFunction(Q,i,Qtot,Eam ):
    Q=Q
    H=computeDropHeight(Qtot,Eam)
    #pertes = 0.5*math.exp(-5)*Q*Q
    if(discret5 and Q%5 != 0):
        return -1
    #if i=0 then it is the deversing valve so just return 0
    #if Q=0 just return 0 because if we use the power evaluations functions, it does'nt return 0 beacause of the modelisation.
    if(i==0 or Q==0):
        return 0
    #If Q> max flow for this turbine, it's an unbreakable constraint so return -1
    if(Q>Sn[i]):
        return -1
    
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
    #Tests with another evaluation function
    #return 0.002989 * Qtot +137.6
    
#Last stage of dynamic programming algorithm
def StageN(Qtot, Eam):
    track[NBstages-1]=[]
    for i in range(Qtot+1):
        #print(costFunction(i,NBstages-1))
        track[NBstages-1].append([i,costFunction(i,NBstages-1,Qtot, Eam),i])
    #Launch recursion for all stage 
    return allStage(track,NBstages-1,Qtot, Eam)

#track is the table of complete subproblems, Stage is the identifiant number of the current stage, Qtot is the total flow, Eam is the uphill level
#(Backward pass)
def allStage(track, stage,Qtot, Eam):
    #print(stage)
    table=[0]*(math.ceil((Qtot+1)))
    track[stage-1]=[]
    
    #for all possible flow values , make the dynamic programming table
    for i in range(Qtot+1):
        table[i]=[]
        bestRank_Value = (0,0)
        #for all possible flow values, calculate the power generated
        for j in range(Qtot+1):
            if(i>=j):
                value=track[stage][i-j][1]+costFunction(j,stage-1,Qtot, Eam)
                table[i].append(value)
                if(value > bestRank_Value[1]):
                    bestRank_Value=(j,value)
            else:
                table[i].append(-1)
        track[stage-1].append([i,bestRank_Value[1],bestRank_Value[0]]) 
    #if made all dynamic programming tables just return the list of all stages dynamic programming table
    if(stage==1):
        return track
    #else, compute the next dynamic programming table
    else:
        return allStage(track, stage-1,Qtot, Eam)

#after making all dynamic programming tables we use it and we build the optimal solution by forward pass
def computeFinalSolution(track,Qtot):
    Solution=[]
    Cost=(track[0][Qtot][1])
    Solution.append(track[0][Qtot][2])
    #print(track[0][Qtot])
    Ressources=Qtot-track[0][(Qtot)][2]
    for i in range(1,len(track)) :
        if Ressources >= Qtot:
            Solution.append(track[i][Qtot][2])
            Ressources-=track[i][Qtot][2]
        else:
            for j in track[i]:
                if j[0]==Ressources:
                    Solution.append(j[2])
                    Ressources-=j[2]
                    break
    return (Solution, Cost)
 
#just a testing function in order to test the algorithm with the 200 values picked in the excel file.
def launchAlgorithme():
    with open('TestingValues') as f:
        lines = f.readlines()
        for i in lines:
            if(i[:1]=='#'):
                print(i)
            else:
                values=i.split(";")
                Qtot=int(values[0].split('.')[:1][0])
                Qvan=values[2]
                eam=float(values[3])
                Q1=values[4]
                Q2=values[6]
                Q3=values[8]
                Q4=values[10]
                Q5=values[12]
                Ptot = float(values[5])+float(values[7])+float(values[9])+float(values[11])+float(values[13])
                
                track=StageN(Qtot, eam)
                turbine, puissance = (computeFinalSolution(track,Qtot))
                ecart=-round(((Ptot-puissance)/Ptot)*100,2)
                print("Débit total : "+str(Qtot)+" Elevation amont : "+str(eam))
                print("Débit turbine 1 : "+str(turbine[1]) +" m3/s\t"+Q1+" m3/s")
                print("Débit turbine 2 : "+str(turbine[2])+" m3/s\t"+Q2+" m3/s")
                print("Débit turbine 3 : "+str(turbine[3])+" m3/s\t"+Q3+" m3/s")
                print("Débit turbine 4 : "+str(turbine[4])+" m3/s\t"+Q4+" m3/s")
                print("Débit turbine 5 : "+str(turbine[5])+" m3/s\t"+Q5+" m3/s")
                print("Débit vanne : \t" + str(turbine[0])+" m3/s\t\t"+Qvan+" m3/s")
                print("Puissance produite : "+str(round(puissance,2)) + " MW\t"+str(round(Ptot,2))+" MW\nÉcart : "+str(ecart)+"%")
    
#function which is returning result of computation to the graphical user interface
#it takes in arguments Total flow (Qtot, uphill), level (eam), QLim is an array of maximum flow to be turbinated by each turbine, discretisation is a boolean wich represent if the flow discretization is 1m3/s or 5m2/s
def runSimulation(Qtot, eam, Qlim, discretization):
    global discret5
    if(discretization):
        discret5 = True
        Qtot=int(5 * round(float(Qtot)/5))
    else:
        discret5=False
        
    global Sn
    Sn=Qlim
    track=StageN(Qtot, eam)
    turbine, puissance = (computeFinalSolution(track,Qtot))
    return (turbine, puissance)



#launchAlgorithme(813,172.192)
#launchAlgorithme()
#print(computeDropHeight(Qtottmp,Eamtmp))
