def loadDelicous(path='data/delicious'):
    '''
    reads tab-deliminated dataset of delicious tags and tag ids
    outputs into dictionary
    path is a string 
    '''
    # get tags and tag ids
    tags = {}
    for line in open(path+'/tags.csv'):
        (t_id,tag)=line.split(',')[0:2]
        tags[t_id]=tag
    return tags

def loadBookmarks(path='data/delicious'):
    # load bookmarks 
    bookmarks={}
    for line in open(path+'/bookmarks.csv'):
        (b_id,md5,title,url)=line.split(',')[0:4]
        bookmarks[b_id]=url
    return bookmarks
    
def loadPairs(tags,bookmarks,path='data/delicious'):    
    '''
    tags is dictionary of tag id and tags
    bookmarks is a dictionary of bookmarks and ids
    '''
    # load pairs
    pairs= {}
    with open(path+'/bookmark_tags.csv') as f:
        next(f)
        for line in f:
            (bookmark_id,tag_id,tagWeight)=line.split(',')[0:3]
            name_url = bookmarks[bookmark_id]
            pairs.setdefault(name_url,{})
            pairs[name_url][tags[tag_id]]=int(tagWeight)
    
    return pairs
        
def usertagged(tags,bookmarks,path='data/delicious'):
    '''
    tags is dictionary of tag id and tags
    bookmarks is a dictionary of bookmarks and ids
    '''
    # Load data user preferences
 
    tagged = {}
    with open(path+'/user_taggedbookmarks-timestamps.csv') as f:
        next(f)
        for line in f:
            (user_id,bkmk_id,tg_id)=line.split(',')[0:3]
            tagged.setdefault(user_id,{})
            tagged[user_id][bookmarks[bkmk_id]]=tags[tg_id]
        
    return tagged


def initializeUserDict(tag,pairsflip,tagged):
    '''
    pairsflip is the pairs dictionary with url and tag flipped
    tag is the string of specified tag
    tagged is a dictionary of user ids, tags, and urls
    '''
    user_dict = {}
    # find all users who posted tag
    for user in tagged: # returns tags
        for p1 in pairsflip[tag]: #returns urls with specified tag

            if p1 in tagged[user]:
                user_dict[user]={}
    return user_dict

def fillItems(user_dict,tagged):
    '''
    user_dict is initialized user dictionary
    tagged is dictionary of users, urls, and tags
    returns filled user_dict
    '''
    all_items = {}
    #find links posted by all users
    for user in user_dict:
        for url in tagged[user]:
            user_dict[user][url]=1.0
            all_items[url]=1
    # fill in missing items with 0
    for ratings in user_dict.values():
        for item in all_items:
            if item not in ratings:
                ratings[item]=0.0
    

    

