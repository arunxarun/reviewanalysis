'''
Created on Jan 4, 2014

@author: jacoba100
'''

from sitejabberreviews import SiteJabberReviews
import matplotlib.pyplot as plt
import re
from nltk.probability import ConditionalFreqDist
from nltk.corpus import stopwords
from nltk import data as nltkdata
from nltk.tokenize.punkt import PunktWordTokenizer
class AnalyzeSiteData(object):
    
    def plotReviews(self, reviews):
        
        reviewsByRating = reviews.reviewsByRating
        xvals = [x for x in reviewsByRating.keys()]
        yvals = [len(reviewsByRating[key]) for key in reviewsByRating.keys()]
        
        plt.plot(xvals,yvals)
        plt.show()
        
    
    def generateCFD(self,reviews):
        
        reviewsByRating = reviews.reviewsByRating
        sortedRatings = sorted(reviewsByRating.keys())
        sent_detector = nltkdata.load('tokenizers/punkt/english.pickle')
        pwt = PunktWordTokenizer()
        cleanTextByRating = {}
        for rating in sortedRatings:
            textBag = []
            
            print "rawRating = %d"%rating
            print "review count = %d"%len(reviewsByRating[rating])
        
            # build up a bag of all words in all reviews for this rating    
            for reviews in reviewsByRating[rating]:
                rawText = reviews.text
                
                sentences = sent_detector.tokenize(rawText)
                for sentence in sentences:
                    lowered = sentence.lower()
                    parts = pwt.tokenize(lowered)
                    # the last word in the sentence always has a period. Remove it
                    parts[-1] = parts[-1][:-1]
                    
                    textBag.extend(parts)
        
            # remove stop words
            cleanTextByRating[rating] = [w for w in textBag if w not in stopwords.words('english')]
            
            
        # build up the CFD of words across specfic ratings. 
                
        cfd = ConditionalFreqDist([(rating,word) for rating in sortedRatings for word in cleanTextByRating[rating]])
        
        return cfd
        
if __name__ == '__main__':
    
#    pageUrls = ['put relative urls here, base url will be in review page parser class']
#    filenames = ['put filenames here, one filename per pageurl']
    pageUrls = ['reviews/www.zulily.com','reviews/www.zappos.com']
    filenames = ['/Users/jacoba100/data/reviews/zulily.pkl','/Users/jacoba100/data/reviews/zappos.pkl']
    
    for i in range(len(pageUrls)):
        print "site: %s"%pageUrls[i]
        sjr = SiteJabberReviews(pageUrls[i],filenames[i])
        sjr.load()
        
        
        asd = AnalyzeSiteData()
        
        asd.plotReviews(sjr)
        
        cfd = asd.generateCFD(sjr)



        
    