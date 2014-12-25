
#index as key , name as value
def read_authors_dict():
    infile = open("data/authors.txt","r")
    infile.readline()
    authors_dict = {}
    for line in infile:
        fields = line.strip().split('|')
        if int(fields[0]) not in authors_dict:
            authors_dict[int(fields[0])] = fields[1]
    infile.close()
    return authors_dict


#index as key, interest field as value
def read_interests_dict():
    interests_dict = {}
    infile = open("data/interests_dict.txt","r")
    for line in infile:
        fields = line.strip().split('|')
        if int(fields[0]) not in interests_dict:
            interests_dict[int(fields[0])] = fields[1]
    infile.close()
    return interests_dict


# convert the recovered matrix from matrix completion into meaningful knowledge
def illustrate_output(authors_dict,interests_dict):
    infile = open("data/2014/mf/recovered_matrix.txt","r")
    infile2 = open("data/2014/combined_matrix.txt","r")
    outfile = open("data/2014/mf/recovered_result.txt","w")
    lines = infile.readlines()
    lines2 = infile2.readlines()
    print len(lines)
    print len(lines2)
    length = len(lines)
    for i in range(length):
        index = 0
        fields = lines[i].strip().split(' ')
        fields2 = lines2[i].strip().split(' ')
        outfile.write(authors_dict[int(fields2[0])]+'|')
        for field in fields[64:]:
            if float(field) > 0:
                outfile.write(interests_dict[index]+'|')
            index += 1
        outfile.write('\n')
    outfile.close()
    infile.close()
    infile2.close()
                



if __name__ == '__main__':
    authors_dict = read_authors_dict()
    interests_dict = read_interests_dict()
    illustrate_output(authors_dict,interests_dict)
