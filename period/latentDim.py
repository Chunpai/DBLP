#run deepwalk module to get the latent dimension 
from subprocess import call
import multiprocessing as mp


def combine_all_edgelist():
    outfile = open('data/all_edgelist.txt','w')
    for year in reversed(xrange(1998,2015,4)):
        infile = open('data/'+str(year)+'_edgelist.txt','r')
        for line in infile:
            outfile.write(line)
        infile.close()
    outfile.close()


def externalCall():
    call(["deepwalk","--format","edgelist","--input","data/all_edgelist.txt","--output","data/all_latentRep3.txt","--workers","4"])
    

if __name__ == "__main__":
    combine_all_edgelist()
    externalCall()
   
