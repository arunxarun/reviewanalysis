'''
Created on Jan 4, 2014

@author: jacoba100
'''
import re
import pickle

class Review(object):
        
    def __init__(self,text,rawRating):
        self.text = text
        
        exp = re.compile("(.*)\.0")
        match  = exp.match(rawRating)
        self.rating = int(match.group(1))
        
        
        
class ReviewContainer(object):
    
    def __init__(self,base,pageUrl,filename):
       
        self.base = base 
        self.pageUrl = self.base + pageUrl
        self.filename = filename
        self.reviewsByRating = {}    
        
        
    def load(self):
        with open(self.filename,'r') as f:
            self.reviewsByRating = pickle.load(f)
        return self.reviewsByRating 
    
    def saveToDisk(self):
        with open(self.filename,'w') as f:
            pickle.dump(self.reviewsByRating,f)
            
    def download(self,save=True):
        raise Exception('implement this in base class!')
           
        