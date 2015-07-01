import re

def loadArtists(path='data/audioscrobbler'):
    # load artists and artist ids 
    artists = {}
    with open(path+'/artist_data.txt') as f:
        for line in f:
            string = [(s.strip()) for s in line.split('\t')][0:2]
            if string[0]=="" or len(string) < 2: continue 
            artists[string[0]]=string[1]
    return artists
             
def loadUserplays(artists,badart,path='data/audioscrobbler'):
    '''
    artists is dictionary of artist id and artists
    '''
    # Load data user preferences
 
    plays = {}
    with open(path+'/user_artist_data_test.txt') as f:
        for line in f:
            string = [(s.strip()) for s in line.split()][0:3]
            if string[0]=="" or len(string) < 3: continue 
            plays.setdefault(string[0],{})
            if string[1] in artists: artist_name = artists[string[1]]
            elif string[1] in badart: artist_name = artists[badart[string[1]]]
            else: artist_name = string[1]  
            #plays[user][artist_name]=playcount    
            plays[string[0]][artist_name]=int(string[2])
        
    return plays            

def findBadartists(path='data/audioscrobbler'):
    '''
    load bad artist ids matched with good_ids
    '''
    badart = {}
    for line in open(path+'/artist_alias.txt'):
        (bad_id,good_id)=[(s.strip()) for s in line.split('\t')][0:2]
        badart[bad_id] = good_id
    return badart
                                
        