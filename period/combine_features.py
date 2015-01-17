
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
            interests_dict[fields[1]] = str(int(fields[0])-1)
    infile.close()
    return interests_dict


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


def extract_test_latentRep(author_interest_dict):
    infile = open("data/all_latentRep3.txt","r")
    infile.readline()
    outfile = open("data/extracted_matrix.txt","w")
    for line in infile:
        fields = line.strip().split(" ")
        index = '{:01}'.format(int(fields[0][4:]))
        if index in author_interest_dict:
            outfile.write(line)
    infile.close()
    outfile.close()


#read latentRep for each labeled author, and extent it with interest list
def combine_latentRep(author_interest_dict):
    infile = open("data/extracted_matrix.txt","r") 
    outfile = open("data/combined_matrix.txt","w")
    for line in infile:
        fields = line.strip().split(" ")
        index = '{:01}'.format(int(fields[0][4:]))
        if fields[0][:4] == '2014':
            fields.extend(author_interest_dict[index])
        else:
            fields.extend([0.0]*24)
        for f in fields:
            outfile.write(str(f)+' ')
        outfile.write('\n')
    outfile.close()
    infile.close() 


if __name__ == '__main__':
    authors_dict = read_authors_dict()
    interests_dict = read_interests_dict()
    author_interest_dict = build_author_interest_dict(interests_dict,authors_dict)
    extract_test_latentRep(author_interest_dict)
    combine_latentRep(author_interest_dict)

