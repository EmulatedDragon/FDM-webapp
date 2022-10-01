import numpy as np
def deflection_calculate(Loads,nodes,E,I,L):  
    #nodes = 4    #the number of nodes excluding the first and last node
    #E=210.0            #taken in giga pascal
    #I=106.67        #taken in (X 10^-9) m^4    
    #L=1

    I/=1000  #give I is in mm^4 to convert to m^4 we divide by 10^12 but we are taking unit of 10^-9 so it is 10^-3

    L/=1000
    last=nodes-1
    h=L/(nodes+1)
    A = np.zeros((nodes, nodes))
    B = np.zeros((1,nodes))
    for i in range(nodes):
        B[0,i]=Loads[i]

    A[0,0]=5            #first row
    A[0,1]=-4
    A[0,2]=1

    A[1,0]=-4            #second row
    A[1,1]=6
    A[1,2]=-4
    A[1,3]=1

    A[last-1,last-3]=1            #second last row
    A[last-1,last-2]=-4
    A[last-1,last-1]=6
    A[last-1,last]=-4

    A[last,last-2]=1        #LAST row
    A[last,last-1]=-4
    A[last,last]=5

    if (2<nodes-2):
        for i in range(2,nodes-2):
            A[i,i-2]=1
            A[i,i-1]=-4
            A[i,i]=6
            A[i,i+1]=-4
            A[i,i+2]=1

    Y=np.matmul(B,np.linalg.inv(A))
    Y*=(h*h*h)*1000/(E*I)
    #for i in range(nodes):
        #print(Y[0,i])             #deviation from real values is half times
    return np.transpose(Y)
