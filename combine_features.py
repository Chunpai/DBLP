
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
    #infile = open("data/interests_dict.txt","r")
    infile = open("data/subDomain.txt","r")
    for line in infile:
        fields = line.strip().split('|')
        if fields[1] not in interests_dict:
            interests_dict[fields[1]] = str(int(fields[0])-1)
    infile.close()
    return interests_dict


"""
#read author dict
def build_author_interest_dict(interests_dict,authors_dict):
    infile = open("data/labeled_authors_info.txt","r")
    flag = 0
    length = len(interests_dict)
    author_interest_dict = {}
    for line in infile:
        interests_list = [-0.1]*length  #for each author create a interests_list
        score = 0.5
        fields = line.strip().split("|")
        for field in fields:
            if "Citations" in field:
                flag = 1
            else:
                if flag == 1:
                    if field != '':
                        if field in interests_dict:
                            index = int(interests_dict[field])
                            interests_list[index] = score 
                            #score -= 0.3
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
"""
def build_author_interest_dict(interests_dict, authors_dict):
    infile = open("data/labeled_authors_info.txt","r")
    author_interest_dict = {}
    for line in infile:
        interests_list = [-0.1]*24  #for each author create a interests_list
        fields = line.strip().split("|")
        author = fields[0]
        for field in fields[1:-1]:
            if field in interests_dict:
                index = int(interests_dict[field])
                interests_list[index] = 0.1
            else:
                print field
                raise SyntaxError
        if fields[0] not in author_interest_dict:
            index = authors_dict[fields[0]]
            author_interest_dict[index] = interests_list
    print len(author_interest_dict)
    return author_interest_dict



#read latentRep for each labeled author, and extent it with interest list
def combine_latentRep(author_interest_dict):
    infile = open("data/2014/latentRep.txt","r") 
    infile.readline()
    outfile = open("data/2014/combined_matrix.txt","w")
    for line in infile:
        fields = line.strip().split(" ")
        if fields[0] in author_interest_dict:
            fields.extend(author_interest_dict[fields[0]])
            for f in fields:
                outfile.write(str(f)+' ')
            outfile.write('\n')
    outfile.close()
    




if __name__ == '__main__':
    authors_dict = read_authors_dict()
    interests_dict = read_interests_dict()
    author_interest_dict = build_author_interest_dict(interests_dict,authors_dict)
    combine_latentRep(author_interest_dict)

