#map all keywords to each subDomain
import codecs

def get_keywords_subDomain_dict():
    infile = codecs.open('subDomain/subDomain.txt','r','utf-8')
    keywords_subDomain_dict = {}
    for line in infile:
        fields = line.strip().split('|')
        infile2 = codecs.open('subDomain/'+fields[1]+'.txt','r','utf-8')
        for line2 in infile2:
            if line2[:-1] not in keywords_subDomain_dict:
                keywords_subDomain_dict[line2[:-1]] = [fields[1]]  
            else:
                keywords_subDomain_dict[line2[:-1]].append(fields[1])
    infile.close()
    infile2.close()
    return keywords_subDomain_dict


if __name__ == "__main__":
    keywords_subDomain_dict = get_keywords_subDomain_dict()
    outfile = codecs.open('keywords_subDomain.txt','w','utf-8')
    for key in keywords_subDomain_dict:
        outfile.write(key+'|')
        for subDomain in keywords_subDomain_dict[key]:
            outfile.write(subDomain+'|')
        outfile.write('\n')
    outfile.close()    
