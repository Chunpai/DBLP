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



def author_interest_output_dict():
    infile = open("data/2014/mf/recovered_matrix3.txt","r")
    author_interest_output_dict = {}
    for line in infile:
        interest_index = 0
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


def eval(author_interest_dict,author_interest_output_dict):
    size = len(author_interest_dict)
    net_accuracy = 0
    count = 0
    for author in author_interest_output_dict:
        real = author_interest_dict[author]
        print real
        length_real = len(real)
        predict = author_interest_output_dict[author]
        print predict
        length_intersection = len(set(real).intersection(predict))
        length_union = len(set(real).union(predict))
        accuracy = length_intersection / float(length_real)
        net_accuracy += accuracy
    print net_accuracy / float(size)


if __name__ == '__main__':
    authors_dict = read_authors_dict()
    interests_dict = read_interests_dict()
    author_interest_dict = build_author_interest_dict(interests_dict,authors_dict)
    author_interest_output_dict = author_interest_output_dict()
    eval(author_interest_dict,author_interest_output_dict)
