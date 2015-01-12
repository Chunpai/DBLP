from keywords_subDomain import get_keywords_subDomain_dict
import codecs
from numpy import array
from scipy.cluster.vq import kmeans
import numpy as np

#data = array([1,1,1,1,2,2,2,2,3,3,3,3])
#kmeans(data,3)

def get_author_interest_dict():
    keywords_subDomain_dict = get_keywords_subDomain_dict()
    author_interest_dict = {}
    for i in range(1,25):
        infile = codecs.open('keywords/'+str(i)+'.txt','r','utf-8')
        for line in infile:
            fields = line.strip().split('|')
            author = fields[0]
            if author not in author_interest_dict:
                author_interest_dict[author] = {}
                for f in fields[1:-2]:
                    if f in keywords_subDomain_dict:
                        subDomains = keywords_subDomain_dict[f]
                        for sub in subDomains:
                            if sub not in author_interest_dict[author]:
                                author_interest_dict[author][sub] = 1
                            else:
                                author_interest_dict[author][sub] += 1
                    else:
                        print f
        infile.close()
    return author_interest_dict                    



#use kmeans to cluster one author's interests
#and assign top cluster of interests to this author
def kmeans_clustering(author_interest_dict):
    infile = codecs.open('labeled_authors_info.txt','r','utf-8')
    author_top_interest_dict = {}
    for line in infile:
        fields = line.strip().split('|')
        author = fields[0]
        if author not in author_top_interest_dict:
            author_top_interest_dict[author] = {}
            interests = []
            for i in author_interest_dict[author].itervalues():
                interests.append(i)
            r1,r2 = kmeans(array(interests),3)
            index = np.where(r1 == r1.max())[0][0]
            for key,value in author_interest_dict[author].iteritems():
                distances = abs(r1-value)
                index2 = np.where(distances == distances.min())[0][0]
                if index2 == index:
                    author_top_interest_dict[author][value] = key
    return author_top_interest_dict
         
        

    



if __name__ == "__main__":
    author_interest_dict = get_author_interest_dict()
    print author_interest_dict['Mihir Bellare']
    author_top_interest_dict = kmeans_clustering(author_interest_dict)
    print author_top_interest_dict['Mihir Bellare']
