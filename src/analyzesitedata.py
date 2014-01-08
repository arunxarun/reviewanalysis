'''
Created on Jan 4, 2014

@author: jacoba100
'''

from sitejabberreviews import SiteJabberReviews
import matplotlib.pyplot as plt
import re
from nltk.probability import ConditionalFreqDist
from nltk.corpus import stopwords

if __name__ == '__main__':
    
    pageUrls = ['put relative urls here, base url will be in review page parser class']
    filenames = ['put filenames here, one filename per pageurl']
    
    
    for i in range(len(pageUrls)):
        print "site: %s"%pageUrls[i]
        sjr = SiteJabberReviews(pageUrls[i],filenames[i])
        reviewsByRating = sjr.load()
        
        sortedRatings = sorted(reviewsByRating.keys())
        xvals = [x for x in reviewsByRating.keys()]
        yvals = [len(reviewsByRating[key]) for key in reviewsByRating.keys()]
        
        plt.plot(xvals,yvals)
        plt.show()
        
        cleanTextByRating = {}
        
        for rating in sortedRatings:
            textBag = []
            
            print "rawRating = %d"%rating
            print "review count = %d"%len(reviewsByRating[rating])
        
            # build up a bag of all words in all reviews for this rating    
            for reviews in reviewsByRating[rating]:
                rawText = reviews.text
                sentences = re.split('[\.\(\)?!&]',rawText)
                for sentence in sentences:
                    lowered = sentence.lower()
                    parts = lowered.split()
                    textBag.extend(parts)
        
            # remove stop words
            cleanTextByRating[rating] = [w for w in textBag if w not in stopwords.words('english')]
            
            
        # build up the CFD of words across specfic ratings. 
                
        cfd = ConditionalFreqDist([(rating,word) for rating in sortedRatings for word in cleanTextByRating[rating]])
    
        for rating in sortedRatings:
            print "rating:%d"%rating
            print cfd[rating]
    