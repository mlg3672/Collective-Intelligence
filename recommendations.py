from math import sqrt

def sim_distance(prefs,person1,person2):
    '''
    person1 and person2 are keys to prefs
    prefs is a dictionary of strings that includes preferences with person1 and person2 as keys
    Returns a Euclidean distance similarity score for person1 and person2 for prefs
    '''
    
    #Get the list of shared_items
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    # if they have no ratings in common, return 0
        if len(si)==0: return 0
    # add up squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in si])
    return 1/(1+sqrt(sum_of_squares))
 
def sim_pearson(prefs,p1,p2):
    '''
    p1 and p2 are keys of the dictionary prefs
    returns the Pearson correlation coeffient for p1 and p2
    '''
    
    # Get a list of the mutually related items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1
    
    # Find the number of elements
    n = len(si)
    # If there are no ratings in common, return 0
    if n==0: return 0
    
    # add up all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    
    # sum squares of prefs
    sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])
    
    # sum the products
    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si]) 
    
    
    # calculate Pearson Score
    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0
    r = num/den
               
    return r           

def simTanimoto(prefs,p1,p2):
    '''
    p1 and p2 are (users) keys of the dictionary prefs
    returns the Jacard similarity coefficient or Tanimoto score for p1 and p2
    '''
    # Get a list of the mutually related items and non-related items
    si = {}
    nsi = {}
    nni = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1
        else: nsi[item]=1
    for it in prefs[p2]:
        if it not in prefs[p1]: nni[item]=1
    # Find the number of elements
    n = len(si)
    n1 = len(nsi)
    n2 = len(nni)
    
    # If there are no ratings in common, return 1
    if n==0: return 0
    
    # calculate Jacard simlarity coefficient
    r = n / (n2+ n + n1)
    # 1 is similar and 0 is dissimilar or empty set
    return r
    
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    '''
    returns the best matches for person from the prefs dictionary
    '''
    scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]
    
    # sort the list so highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]

def getRecommendations(prefs,person,similarity=sim_pearson):
    '''
    Gets recommendations for a person by using a weighted average
    of every other user's rankings
    '''
    totals={}
    simSums={}
    for other in prefs:

        # don't compare me to myself
        if other==person: continue
        sim=similarity(prefs,person,other)

        # ignore scores of zero or lower
        if sim<=0: continue
        for item in prefs[other]:
        
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity * Score
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
      
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim
                
    # Create the normalized list
    rankings=[(total/simSums[item],item) for item,total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
                
            # Flip item and person
            result[item][person]=prefs[person][item]
    return result

def calculateSimilarItems(prefs,n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result={}
    # Invert the preference matrix to be item-centric
    itemPrefs=transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        # Status updates for large datasets
        c+=1
        if c%100==0: print("%d / %d" % (c,len(itemPrefs)))
        # Find the most similar items to this one
        scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
        result[item]=scores
    return result

def getRecommendedItems(prefs,itemMatch,user):
    '''
    Gets recommendations for a person by using a weighted average
    of every other user's rankings
    '''
    userRatings=prefs[user]
    scores={}
    totalSim={}
    # Loop over items rated by this user
    for (item,rating) in userRatings.items( ):
        # Loop over items similar to this one
        for (similarity,item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings: continue
            # Ignore if no similarity to avoid division by zero
            if similarity ==0: 
                continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating
            # Sum of all the similarities
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity

    # Divide each total score by total weighting to get an average
    rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

    # Return the rankings from highest to lowest
    rankings.sort( )
    rankings.reverse( )
    return rankings

def loadMovieLens(path='data/movielens'):
    # Get movie titles
    movies={}
    for line in open(path+'/movies.txt'):
        (id,title)=line.split(',')[0:2]
        movies[id]=title
  
    # Load data
    prefs={}
    for line in open(path+'/ratings.txt'):
        (user,movieid,rating,ts)=line.split(',')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]]=float(rating)
    return prefs

def calculateSimilarUsers(prefs,n=5):
    '''
    user prefs dictionary for precomputing 
    user similarities and returning only the top five
    '''
    result={}
    c=0
    for user in prefs:
        # Status updates for large datasets
        c+=1
        if c%100==0: print("%d / %d" % (c,len(prefs)))
        # Find the most similar items to this one
        scores=topMatches(prefs,user,n=n,similarity=sim_distance)
        result[user]=scores
    return result    
    
# A dictionary of movie critics and their ratings of a small set of movies\n",
# set of movies

critics = {'Lisa Rose':{'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck':3.0,'Superman Returns': 3.5, 'You, Me and Dupree':2.5,'The Night Listener':3.0},'Gene Seymour':{'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck':1.5,'Superman Returns': 5.0, 'You, Me and Dupree':3.5,'The Night Listener':3.0},'Michael Phillips':{'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,'Superman Returns': 3.0,'The Night Listener':4.0},'Claudia Puig':{'Snakes on a Plane': 3.5, 'Just My Luck':3.0,'Superman Returns': 4.0, 'You, Me and Dupree':2.5,'The Night Listener':4.5},'Mick LaSalle':{'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck':2.0,'Superman Returns': 3.0, 'You, Me and Dupree':2.0,'The Night Listener':3.0},'Jack Matthews':{'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Superman Returns': 5.0, 'You, Me and Dupree':3.5,'The Night Listener':3.0},'Toby':{'Snakes on a Plane': 4.5,'Superman Returns': 4.0, 'You, Me and Dupree':1.0},'Michele':{'Lady in the Water': 4.0, 'Snakes on a Plane': 3.5}}
