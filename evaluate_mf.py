import random
from numpy import array
from scipy.cluster.vq import kmeans
import numpy as np

#author name as key , and index as value
def read_authors_dict():
    infile = open("data/authors.txt","r")
    infile.readline()
    authors_dict = {}
    for line in infile:
        fields = line.strip().split('|')
        if fields[1] not in authors_dict:
            authors_dict[fields[1]] = fields[0]
    infile.close()
    return authors_dict


#interest name as key, and index as value
def read_interests_dict():
    interests_dict = {}
    infile = open("data/subDomain.txt","r")
    for line in infile:
        fields = line.strip().split('|')
        if fields[1] not in interests_dict:
            #interests_dict[fields[1]] = str(int(fields[0])-1)
            interests_dict[fields[1]] = fields[0]
    infile.close()
    return interests_dict



#different from build_author_interest_dict in combine_feature.py
def build_author_interest_dict(interests_dict, authors_dict):
    infile = open("data/labeled_authors_info.txt","r")
    author_interest_dict = {}
    for line in infile:
        interests_list = []  #for each author create a interests_list
        fields = line.strip().split("|")
        author = fields[0]
        for field in fields[1:-1]:
            if field in interests_dict:
                index = int(interests_dict[field])
                interests_list.append(index)
            else:
                print field
                raise SyntaxError
        if fields[0] not in author_interest_dict:
            index = authors_dict[fields[0]]
            author_interest_dict[index] = interests_list
    print len(author_interest_dict)
    return author_interest_dict


"""
def author_interest_output_dict():
    infile = open("data/2014/mf/recovered_matrix4.txt","r")
    author_interest_output_dict = {}
    for line in infile:
        interest_index = 1
        fields = line.strip().split(' ')
        if fields[0] not in author_interest_output_dict:
            author_interest_output_dict[fields[0]] = []
        else:
            print 'error'
        for f in fields[65:]:
            if float(f) > 0:
                author_interest_output_dict[fields[0]].append(interest_index)
            interest_index += 1
    infile.close()
    return author_interest_output_dict
"""
def author_interest_output_dict():
    infile = open("data/2014/mf/new_recovered_matrix16.txt","r")
    author_interest_output_dict = {}
    for line in infile:
        interest_index = 1
        fields = line.strip().split(' ')
        author = fields[0]
        if author not in author_interest_output_dict:
            author_interest_output_dict[author] = []
        else:
            print 'error'
        interests = [float(i) for i in fields[65:]]
        r1, r2 = kmeans(array(interests),3)
        index = np.where(r1 == r1.max())[0][0]
            
        for i in range(24):
            distances = abs(r1-interests[i])
            index2 = np.where(distances == distances.min())[0][0]
            if index2 == index:
                author_interest_output_dict[author].append(i+1)
    infile.close()
    return author_interest_output_dict



def eval(author_interest_dict,author_interest_output_dict):
    size = len(author_interest_dict)
    net_precision = 0
    net_accuracy = 0
    net_recall = 0
    net_F_score = 0
    count = 0
    for author in author_interest_output_dict:
        print 'author:',author
        real = author_interest_dict[author]
        print 'real',real
        length_real = len(real)
        predict = author_interest_output_dict[author]
        print 'predict',predict
        length_intersection = len(set(real).intersection(predict))
        length_union = len(set(real).union(predict))
        precision = length_intersection / float(len(predict))
        recall = length_intersection / float(len(real))
        if (precision + recall) != 0:
            F_score = 2*precision*recall / (precision+recall)
        else:
            F_score = 0
        accuracy = length_intersection / float(length_real)
        net_accuracy += accuracy
        net_precision += precision
        net_recall += recall
        net_F_score += F_score
    print 'accuracy', net_accuracy / float(size)
    print 'precision',net_precision / float(size)
    print 'recall',net_recall / float(size)
    print 'F_score',net_F_score / float(size)


if __name__ == '__main__':
    authors_dict = read_authors_dict()
    interests_dict = read_interests_dict()
    author_interest_dict = build_author_interest_dict(interests_dict,authors_dict)
    author_interest_output_dict = author_interest_output_dict()
    eval(author_interest_dict,author_interest_output_dict)
