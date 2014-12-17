import random
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
    infile = open("data/interests_dict.txt","r")
    for line in infile:
        fields = line.strip().split('|')
        if fields[1] not in interests_dict:
            interests_dict[fields[1]] = fields[0]
    infile.close()
    return interests_dict


"""
#return labeled authors dict
# index as key and author name as value
def read_labeled_authors_info(authors_dict):
    infile = open("data/labeled_authors_info.txt","r")
    labeled_authors_dict = {}
    for line in infile:
        fields = line.strip().split("|")
        if fields[0] not in authors_dict:
            print fields[0]
            raise SyntaxError
        else:
            if fields[0] not in labeled_authors_dict:
                labeled_authors_dict[authors_dict[fields[0]]] = fields[0]
    print labeled_authors_dict
    infile.close()
    return labeled_authors_dict
"""


#read author dict
def build_author_interest_dict(interests_dict,authors_dict):
    infile = open("data/labeled_authors_info.txt","r")
    flag = 0   # check the position of scanning cursor
    length = len(interests_dict)
    author_interest_dict = {}
    for line in infile:
        interests_list = []  #for each author create a interests_list
        fields = line.strip().split("|")
        for field in fields:
            if "Citations" in field:
                flag = 1
            else:
                if flag == 1:
                    if field != '':
                        if field in interests_dict:
                            index = int(interests_dict[field])
                            interests_list.append(index)
                        else:
                            raise SyntaxError
                    else:
                        #interests_dict[field][1] += 1
                        flag = 0
        if fields[0] not in author_interest_dict:
            index = authors_dict[fields[0]]
            author_interest_dict[index] = interests_list
    print len(author_interest_dict)
    return author_interest_dict

            
#read latentRep for each labeled author, and extent it with interest list
def generate_M3L_data(author_interest_dict):
    infile = open("data/2014/latentRep.txt","r") 
    infile.readline()
    outfile = open("data/2014/m3l/M3L.dat","w")
    for line in infile:
        fields = line.strip().split(" ")
        if fields[0] in author_interest_dict:
            interest_list = author_interest_dict[fields[0]]
            for index in interest_list[:-1]: #iterate interest list to write index
                outfile.write(str(index)+',')
            outfile.write(str(interest_list[-1]) + ' ')
            length = len(fields)
            for i in range(1,length):
                outfile.write(str(i)+':'+fields[i]+' ')
            outfile.write('\n')
    outfile.close()
    

#random sample some traning data, and rest as testing data
def random_sample():
    size = 200
    random_index_list = random.sample(range(2065), size)
    infile = open("data/2014/m3l/M3L.dat","r")
    outfile = open("data/2014/m3l/train.txt","w")
    outfile2 = open("data/2014/m3l/test.txt","w")
    matrix = []
    index = 0
    for line in infile:
        if index in random_index_list:
            outfile.write(line)
        else:
            outfile2.write(line)
        index += 1
    infile.close()
    outfile.close()
    outfile2.close()



if __name__ == '__main__':
    authors_dict = read_authors_dict()
    interests_dict = read_interests_dict()
    author_interest_dict = build_author_interest_dict(interests_dict,authors_dict)
    generate_M3L_data(author_interest_dict)
    random_sample()
