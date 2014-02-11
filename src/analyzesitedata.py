'''
Created on Jan 4, 2014

@author: jacoba100
'''

from sitejabberreviews import SiteJabberReviews
import matplotlib.pyplot as plt
import re
from nltk.probability import FreqDist
from nltk.probability import ConditionalFreqDist
from nltk.corpus import stopwords
from nltk import data
from nltk import NaiveBayesClassifier
from collections import defaultdict

import random

class AnalyzeSiteData(object):
    
    def plotReviewCounts(self, reviews):
        '''
        generate a plot of rating frequency
        @param reviews: a review object containing all reviews grouped by rating.
        ''' 
        reviewsByRating = reviews.reviewsByRating
        xvals = [x for x in reviewsByRating.keys()]
        yvals = [len(reviewsByRating[key]) for key in reviewsByRating.keys()]
        
        plt.plot(xvals,yvals)
        plt.show()
        
    def textBagFromRawText(self,rawText):
        '''
        @param rawText: a string of whitespace delimited text, 1..n sentences
        @return: the word tokens in the text, stripped of non text chars including punctuation
        '''
        rawTextBag = []        
        sentences = re.split('[\.\(\)?!&,]',rawText)
        for sentence in sentences:
            lowered = sentence.lower()
            parts = lowered.split()
            rawTextBag.extend(parts)
         
        
        textBag = [w for w in rawTextBag if w not in stopwords.words('english')]    
        return textBag
                    
    def generateCFD(self,reviews):
        
        '''
        @param reviews: a ReviewContainer object
        @return: a ConditionalFreqDist object where the child FreqDists by rating
        '''
        reviewsByRating = reviews.reviewsByRating
        sortedRatings = sorted(reviewsByRating.keys())
        
        cleanTextByRating = {}
        for rating in sortedRatings:
            textBag = []
            
#            print "rawRating = %d"%rating
#            print "review count = %d"%len(reviewsByRating[rating])
        
            # build up a bag of all words in all reviews for this rating    
            for reviews in reviewsByRating[rating]:
                textBag.extend(self.textBagFromRawText(reviews.text))
                
        
            # remove stop words
            cleanTextByRating[rating] = [w for w in textBag if w not in stopwords.words('english')]
            
            
        # build up the CFD of words across specfic ratings. 
                
        cfd = ConditionalFreqDist([(rating,word) for rating in sortedRatings for word in cleanTextByRating[rating]])
        
        return cfd
    
    def generateLeftSideFreqDist(self,fd1,fd2):
        '''
        this method traverses two FreqDists, and builds a third one that only contains terms that are in fd1
        but not in fd2, in other words the 'left side' of the two
        @param fd1: the left side of the LHJ
        @param fd2: the right side of the LHJ
        @return: the LHJ
        '''
        
        wordCounts = [(key,fd1[key]) for key in fd1.keys() if key not in fd2]
        
        wordbag = []
        for key, count in wordCounts:
            for i in range(count):
                wordbag.append(key)
                
                
        return FreqDist(wordbag)
    
    
    def generateLearningSetsFromReviews(self,reviews, ratings,buckets):
        '''
        produces a set of data for supervised learning into labeled buckets 
        trainSet is training data
        devSet is data used to correct algorithm
        testSet is data used to test algorithm
        @param reviewsSet: array of ReviewContainer object
        @param ratings: array of ratings to extract reviews with 
        @param buckets: map of names to percentages to break learning data into, must sum to 1
        @return:  bucket map of lists: [(tokenized array of words[], rating)...]
        '''
        
        # check to see that percentages sum to 1
        # get collated sets of reviews by rating. 
        
        val = 0.0
        for pct in buckets.values():
            val += pct
            
        if val > 1.0:
            raise 'percentage values must be floats and must sum to 1.0'
        
        reviewsByRating = defaultdict(list)
            
        for reviewSet in reviews:
            for rating in ratings:
                reviewList = [(self.textBagFromRawText(review.text), rating) for review in reviewSet.reviewsByRating[rating]]
                reviewsByRating[rating].extend(reviewList)
                random.shuffle(reviewsByRating[rating]) # mix up reviews from different reviewSets
            
        
        # break collated sets across all ratings into percentage buckets
        learningSets = defaultdict(list) 
        
        for rating in ratings:
            sz = len(reviewsByRating[rating]) 
            
            lastidx = 0
            for (bucketName, pct) in buckets.items():
                idx=lastidx + int(pct*sz)
                
                learningSets[bucketName].extend(reviewsByRating[rating][lastidx:idx])
                
                lastidx  = idx
                
        return learningSets
         
    
    
    
    def encodeData(self,trainSet,encodingMethod):
        '''
        @param trainSet: the set of tuples structured as (textBag, rating) 
        @param encodingMethod: a function that encodes the data
        @return: a tuple set of encoded data and rating
        '''
        
        return [(encodingMethod(tokenizedText), rating) for (tokenizedText, rating) in trainSet]
             
        
    
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
        
        asd.plotReviewCounts(sjr)
        
        cfd = asd.generateCFD(sjr)



        
    