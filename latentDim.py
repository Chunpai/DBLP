from subprocess import call
import multiprocessing as mp

def externalCall(year):
    call(["deepwalk","--format","edgelist","--input","data/"+str(year)+"/edgelist.txt","--output","data/"+str(year)+"/latentRep.txt"])
    return

if __name__ == "__main__":

    procs = []
    for year in range(2013,2015):
        p = mp.Process(target=externalCall, args= (year,))
        procs.append(p)
        p.start()
    
    #pool = mp.Pool(processes=2)
    #for year in range(1995,1997):
    #    call(["time","deepwalk", "--input","data/"+str(year)+"/edgelist.txt","--output","data/"+str(year)+"/latentRep.txt"])
