import random
import numpy as np

def read_matrix():
    infile = open("data/2014/combined_matrix.txt","r")
    matrix = []
    authors_index = []
    for line in infile:
        fields = line.strip().split(' ')
        authors_index.append(fields[0])
        fields = fields[1:]
        fields = map(float, fields)
        matrix.append(fields)
    infile.close()
    #print matrix
    matrix = np.array(matrix)
    print matrix.shape
    return matrix, authors_index


def random_sample():
    size = 200
    random_index_list = random.sample(range(2065), size)
    infile = open("data/2014/combined_matrix.txt","r")
    matrix = []
    index = 0
    for line in infile:
        flist = []
        fields = line.strip().split(' ')[1:]
        fields = map(float, fields)
        if index in random_index_list:
            matrix.append(fields)
        else:
            for f in fields[:64]:
                flist.append(f)
            for f in fields[64:]:
                flist.append(0.0)
            matrix.append(flist)
        index += 1
    #print matrix
    #print random_index_list
    matrix = np.array(matrix)
    infile.close()
    print matrix.shape
    return matrix



#use SGD to do the matrix factorization
def matrix_factorization(R, P, Q, K, steps=1000, alpha= 0.01, beta= 0.01):
    Q = Q.T
    #iteration = 0
    lowest_error = 300000
    for step in xrange(steps):
        #print step
        #new_alpha = alpha / (step*len(random_numbers)+1)
        #new_alpha = alpha / (step*40+1)
        new_alpha = alpha
        if step >= 500:
            new_alpha = 0.001
        print('step:'+str(step))
        print 'step_length',new_alpha
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] != 0.0:
                    #iteration += 1
                    #new_alpha = alpha / pow(iteration,0.5)
                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                    #print 'eij+'+str(eij)
                    for k in xrange(K):
                        #print P[i][k],Q[k][j]
                        P_temp = P[i][k]
                        #Q_temp = Q[k][j]
                        P[i][k] = P[i][k] + new_alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + new_alpha * (2 * eij * P_temp - beta * Q[k][j])
        #eR = np.dot(P,Q)
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] != 0.0:
                    e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]),2)
                    #e = e + abs(R[i][j] - numpy.dot(P[i,:],Q[:,j]))
                    for k in xrange(K):
                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))                
        print e
        if e < lowest_error:
            lowest_error = e
        else:
            break
    return P, Q.T





if __name__ == "__main__":
    original_matrix, authors_index = read_matrix()
    training_matrix = random_sample()
    row, col = training_matrix.shape
    rank = 16 
    P = np.random.normal(0,1,(row,rank))
    Q = np.random.normal(0,1,(col,rank))
    NP, NQ = matrix_factorization(training_matrix, P, Q, rank)
    completed_matrix = np.dot(NP,NQ.T)
    row, col = completed_matrix.shape
    #outfile1 = open("data/2014/mf/original_matrix.txt","w")
    
        
    outfile = open("data/2014/mf/new_recovered_matrix16.txt","w")
    for i in range(row):
        outfile.write(str(authors_index[i])+' ')
        for j in range(col):
            outfile.write(str(completed_matrix[i][j])+' ')
        outfile.write('\n')
    outfile.close()
    #evaluation(original_matrix, completed_matrix)
    



