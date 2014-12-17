# read the data/labeled_authors_info.txt
# build the interest dictionary, key is field of study
# 
# and save the dictionary as data/interests_dict.txt

def build_interests_dict():
    interests_dict = {}
    index = 0
    flag = 0
    infile = open("data/labeled_authors_info.txt","r")
    outfile = open("data/interests_dict.txt","w")
    for line in infile:
        fields = line.strip().split("|")
        for field in fields:
            if "Citations" in field:
                flag = 1
            else:
                if flag == 1:
                    if field != '':
                        if field not in interests_dict:
                            interests_dict[field] = [index,1]
                            outfile.write(str(index)+'|'+field+'\n')
                            index += 1
                    else:
                        #interests_dict[field][1] += 1
                        flag = 0
    #print interests_dict
    #sorted_dict = sorted(interests_dict.items(), key = lambda x:x[1][1],reverse=True)
    #for item in sorted_dict:
    #    outfile.write(str(item[1][0])+'|'+item[0]+'|'+str(item[1][1])+'\n')
    outfile.close()
    return interests_dict


if __name__ == "__main__":
    build_interests_dict()


                

            
