import re
import random as rd
import math



#------------------------------------------data cleaning------------------------
file=open(r"C:/Users/Osama  Mohammed/Desktop/bbchealth.txt",'r', encoding="utf8")
tweets=list(file)
 
for i in range(len(tweets)):
    tweets[i]=tweets[i][50:]

    tweets[i]=re.sub(r'(http\w?.+)','', tweets[i])

    tweets[i]=re.sub(r'(@\w[A-z0-9]+)', '' ,tweets[i])
 
    tweets[i]=re.sub(r'[^\w\s]','', tweets[i])
    tweets[i]=tweets[i].lower()
     
    tweets[i]=tweets[i].split()
 
file.close() 


#Gets a random tweet that was not picked before
Used = dict()
def GetRandomTweet():  
    idx = rd.randint(0, len(tweets) - 1)
    if (idx in Used):
        idx = GetRandomTweet() 
        
    Used[idx] = True
    return idx  

#Calculates jaccard distance
def CalcJaccard(tweet1, tweet2): 
    intersection = set(tweet1).intersection(tweet2)
    union = set(tweet1).union(tweet2)
    return 1 - (len(intersection) / len(union))  


#Calculates all jaccard distances between all tweets to save time
Distances = dict()
def PreCalculateDistance():
    for t1 in range(len(tweets)):
        Distances[t1] = dict()
        for t2 in range(len(tweets)):
            if (t1==t2):
                Distances[t1][t2] = 0
            else:
                Distances[t1][t2] = CalcJaccard(tweets[t1],tweets[t2])
                

#Assigns each tweet to the nearest centroid
Error = dict()
def AssignTweets(Centroids):
    Clusters = dict()
    for c in range(len(Centroids)):
        Clusters[c] = []
        
    for t in range(len(tweets)):
        bestcluster = -1
        bestdis = math.inf
        for c in range(len(Centroids)):
            dis = Distances[t][Centroids[c]]
            if dis < bestdis:
                bestcluster = c
                bestdis = dis
                
            if (t==Centroids[c]):
                bestcluster = c
                bestdis= dis
                break
        
        Clusters[bestcluster].append(t)
        Error[t] = bestdis * bestdis
        
    return Clusters
  

#Updates centroids with the new best one
def UpdateCentroids(Clusters):
    NewCentroids = []
    for c in range(len(Clusters)):
        BestTotal = math.inf
        BestIdx = -1
        for x in range(len(Clusters[c])):
            TotalDist = 0
            for y in range(len(Clusters[c])):
                TotalDist += Distances[Clusters[c][x]][Clusters[c][y]]
            
            if TotalDist<BestTotal:
                BestTotal = TotalDist
                BestIdx = x
        
        NewCentroids.append(Clusters[c][BestIdx])
        
    return NewCentroids

#Computes the error
def ComputeSSE():
    SSE = 0
    for t in range(len(tweets)):
        SSE = SSE + Error[t]
        
    return SSE


def KMeans(k , maxit = 50):
    Used.clear()
    Centroids = []
    
    for i in range(k):
        idx = GetRandomTweet()
        Centroids.append(idx)
    
    PreviousCentroids = []
    for i in range(maxit):
        Clusters = AssignTweets(Centroids)
        PreviousCentroids = Centroids
        Centroids = UpdateCentroids(Clusters)
       
        if PreviousCentroids == Centroids:
            break
        
    SSE = ComputeSSE()
    return Clusters, SSE

#------------------------main algo---------------------------------------------

PreCalculateDistance()
k = 3
besterror = math.inf
bestk = 0

for i in range(5):
    
    clus,error = KMeans(k)
    if (error<besterror):
        besterror = error
        bestk = k
        
    for c in range(len(clus)):
       print(str(len(clus[c])) + " tweets")

    print("squared sum error: " + str(error))
    print('\n')
    k = k + 1
    
print("Best k value was : " + str(bestk))