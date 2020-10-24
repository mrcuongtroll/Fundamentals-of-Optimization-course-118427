import numpy as np

#Initiate stuff: (You have to change this block of code manually to fit your problem)
c = np.array([[3,2]])
A = np.array([[2,1], [1,2], [1,-1]])
b = np.array([[7],[8],[2]])

def simplex(c, A, b):
    #c: objective coeffs
    #A: constraints coeffs
    #b: constraints
    #Add slack variable:
    N = A                                           #The matrix N
    JN = sorted(list(np.arange(0,A.shape[1],1)))    #Initiate JN here
    A = A.T                                         #Do this so that the work become a lil'ez-er
    mb = b.shape[0]
    mA = A.shape[0]
    for i in range(b.shape[0]):
        c = np.hstack((c, np.array([[0]])))
        A = np.vstack((A, np.zeros((1,mb))))
        A[mA+i][i] = 1
    B = A[mA:]                                      #This is the matrix B
    JB = sorted(list(np.arange(mA, A.shape[0],1)))  #Don't forget JB
    A = A.T                                         #Return to A its original form

    #Tiem 4 SIMPlex:
    while True:
        #Now we make cB:
        c = c.T
        cB = c[JB[0]]
        for i in JB[1:]:
            cB = np.vstack((cB, c[i]))
        cB = cB.T
        #...and cN:
        cN = c[JN[0]]
        for i in JN[1:]:
            cN = np.vstack((cN, c[i]))
        cN = cN.T
        #Return c to its original form
        c = c.T
        #This is where the guide begins
        u = cB.dot(np.linalg.inv(B))
        deltaN = u.dot(N) - cN
        xN = 0
        xB = np.linalg.inv(B).dot(b)
        if (deltaN >= 0).all():
            print("Optimal solution found!")
            break
        else:
            list_deltaN = [float(deltaN[:,i]) for i in range(deltaN.shape[1])]
            p = JN[list_deltaN.index(min(list_deltaN))]
            Y = (np.linalg.inv(B).dot(A[:,p])).reshape((mb,1))
            if (Y <= 0).all():
                print("Objective is unbounded")
                return
            else:
                find_q = [float(xB[i]/Y[i]) for i in range(len(JB))]
                find_q_ex = [float(xB[i]/Y[i]) for i in range(len(JB)) if float(Y[i]) > 0]
                q = JB[find_q.index(min(find_q_ex))]
                #remove q from JB and add p to JB
                JB.remove(q)
                JB.append(p)
                JB.sort()
                #remove p from JN and add q to JN
                JN.remove(p)
                JN.append(q)
                JN.sort()
                #B = A(JB)
                A = A.T
                B = A[JB[0]]
                for i in JB[1:]:
                    B = np.vstack((B,A[i]))
                B = B.T
                #N = A(JN)
                N = A[JN[0]]
                for i in JN[1:]:
                    N = np.vstack((N, A[i]))
                N = N.T
                #Don't forget to give A's original form back to it
                A = A.T
    print(xB)
    print(xN)
    print('f(x) = ' + str(float(cB.dot(xB))))

simplex(c,A,b)