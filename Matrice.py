import numpy as np
import time
import scipy.sparse as sp

def createMatrix(value):
    A = np.zeros((value,value))
    size = value
    rang = (value ** 2) //20
    for i in range(rang):
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
def MapReduce(A,B):

    return C

start_time = time.time()
value = 10000
A = sp.rand(value,value,0.01)
B = sp.rand(value,value,0.01)
A_r = sp.csc_matrix(A)
B_r = sp.csc_matrix(B)
print(B_r.data)
#A.data
#A.indices
#A.indptr 
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
C = np.dot(A_r,B_r)
C1,C2,C3 = MultiplySparseMatrix(A_r,B_r,value)
print(C1,C.indptr)



print("--- %s seconds ---" % (time.time() - start_time))


