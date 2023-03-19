import numpy as np
import time
import scipy.sparse as sp
from collections import defaultdict

def createMatrix(value):
    A = np.zeros((value,value))
    size = value
    for i in range(5*value):
        row = np.random.randint(0,size)
        column = np.random.randint(0,size)
        value = np.random.randint(0,10)
        if row > 0:
            row = row - 1
        if column > 0:
            column = column - 1

        A[row][column] = value
    A_sparse = sp.csc_matrix(A)

    return A_sparse

def MultiplyMatrix(A,B,value):
    C = np.zeros((value, value), dtype=np.uint32)
    for i in range(value):
        for j in range(value):
            for k in range(value):
                C[i][j] += A[i][k] * B[k][j]
 
    return C
def MultiplySparseMatrix(A,B,value):
    C_p = np.zeros(value + 1, dtype=np.uint32)
    C_p[0] = 0
    nz = 0
    count2 = 0
    z = 0
    w = np.zeros(value,dtype=np.uint32)
    fastfree = np.zeros(value,dtype=np.uint32)
    x = np.zeros(value,dtype = np.float32)
    for i in range(value):
        j = B.indptr[i]
        while j < B.indptr[i+1]:
            line = B.indices[j]
            k = A.indptr[line]
            while k < A.indptr[line+1]:
                z = A.indices[k]
                if(w[z] == 0):
                    w[z] = 1
                    fastfree[count2] = z
                    count2 += 1
                    nz += 1
                k +=1
            j +=1
        C_p[i+1] = C_p[i]+ count2
        for ii in range(count2):
            tempo = fastfree[ii]
            w[tempo] = 0
            fastfree[ii]= 0
        count2 = 0
    #Correct pour sur 
    count2 = 0
    count = 0
    C_indices = np.zeros(nz,dtype=np.uint32)
    C_data = np.zeros(nz,dtype=np.float32)
    for i in range(value):
        j = B.indptr[i]
        while j < B.indptr[i+1]:
            value = B.data[j]
            line = B.indices[j]
            k = A.indptr[line]
            while k < A.indptr[line+1]:
                z = A.indices[k]
                if(x[z] == 0):
                    fastfree[count2] = z
                    count2 += 1
                value2 = A.data[k]
                x[z] += value * value2
                k += 1
            j +=1
        for ii in range(count2):
            tempo = fastfree[ii]
            C_indices[count] = tempo 
            C_data[count] = x[tempo] 
            count += 1
            x[tempo] = 0
            fastfree[ii] = 0
        count2 = 0

    return C_p,C_indices,C_data
def Change_Format(A,value):
    new_A = []
    for i in range(value):
        j = A.indptr[i]
        while j < A.indptr[i+1]:
            k = A.indices[j]
            l = A.data[j]
            new_A.append([i,k,l])
            j += 1
    return new_A
def Map_Reduce(A,B,value):
    A1 = Change_Format(A,value)
    B1 = Change_Format(B,value)
    A_Dict = defaultdict(list)
    B_Dict = defaultdict(list)
    for i in range(len(A1)):
        A_Dict[A1[i][1]].append((A1[i][0],A1[i][2]))
    for i in range(len(B1)):
        B_Dict[B1[i][0]].append((B1[i][1],B1[i][2]))
    #OKay
    tempo_Dict = defaultdict(list)
    for i in range(value):
        if i in A_Dict and i in B_Dict:
            for j in A_Dict[i]:
                for k in B_Dict[i]:
                    x = j[0]
                    y = k[0]
                    value = j[1] *k[1]
                    tempo_Dict[(x,y)].append(value)
    C = list()
    for i ,j in tempo_Dict.items():
        C.append([i[0],i[1],sum(j)])
    return C

start_time = time.time()
value = 1000

A_r = createMatrix(value)
B_r = createMatrix(value)
#A.data
#A.indices
#A.indptr 
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
test1 = Map_Reduce(A_r,B_r,value)

print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
test1,test2,test3 = MultiplySparseMatrix(A_r,B_r,value)

print("--- %s seconds ---" % (time.time() - start_time))


