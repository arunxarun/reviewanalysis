'''
Created on Mar 14, 2014

@author: jacoba100
'''


from review import Review
from sitejabberreviews import SiteJabberReviews
from analyzesitedata import AnalyzeSiteData
from operator import itemgetter
import matplotlib.pyplot as plt

from nltk.probability import FreqDist
from nltk.probability import ConditionalFreqDist
import nltk
from nltk.corpus import stopwords
import random
import re
from collections import defaultdict

class BayesHelper(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def increaseReviewData(self,reviews,rating,growthFactor):
    
        '''
        increases data set by sampling with replacement from word distribution of rated reviews.
        @param reviewContainer - contains reviews mapped to ratings
        @param rating - the rating to use to seed and create new reviews.
        @return the increased review set (includes originals)
        '''
        
        newReviews = []
        newReviews.extend(reviews)
        
        ratingCode = "%d.0"%rating
        
        try:
            
            
            allReviewWords = []
            totalReviewLen = 0
            
            for review in reviews:
                bag = self.textBagFromRawText(review.text)
                allReviewWords.extend(bag)
                totalReviewLen += len(bag)
           
            
            reviewCt = len(reviews)
            avgRevLen = totalReviewLen/reviewCt
            
            growthFactor -= 1
            
            # create X reviews of avgRevLen
            for i in range(growthFactor*reviewCt):
                rev = Review(self.createReview(allReviewWords,avgRevLen),ratingCode)
                newReviews.append(rev)
            
#              
            return newReviews
                                
                
        except Exception as inst:
            self.fail(inst)
            
            
    def textBagFromRawText(self,rawText):
        '''
        @param rawText: a string of whitespace delimited text, 1..n sentences
        @return: the word tokens in the text, stripped of non text chars including punctuation
        '''
        textBag = []
        rawTextBag = []        
        try:
            
            sentences = re.split('[\.\(\)?!&,]',rawText)
            for sentence in sentences:
                lowered = sentence.lower()
                parts = lowered.split()
                rawTextBag.extend(parts)
            
            textBag = [w for w in rawTextBag if w not in stopwords.words('english')]
        
        
        except Exception as inst:
            self.fail(inst)
            
        return textBag
    
    
    def buildKFoldValidationSets(self,folds,iteration, reviewsByRating):
        """
        build test and training sets
        @param iteration - the offset of the arrays to hold out
        @param reviewsByRating - the set of reviews to build from
        @return test and training arrays
        """
        
        test = []
        test.extend(reviewsByRating[1][iteration])
        test.extend(reviewsByRating[5][iteration])
        
        training = []
    
        for i in range(folds):
            if i == iteration:
                continue
            training.extend(reviewsByRating[1][i])
            training.extend(reviewsByRating[5][i])

        return training, test
    
    
    
    def createReview(self,textFreqDist,reviewLength):
        """
        @param textFreqDist -  the array containing the frequency distribution of words to choose from.
        @param reviewLength -  the length of the review (in words) to build
        @return the generated review as a string
        """
        randLen = len(textFreqDist)
        reviewStr = ""
        
        for i in range(reviewLength):
            reviewStr += (textFreqDist[random.randint(0,randLen-1)] + ' ')
        
        return reviewStr
    
    
    def partitionArray(self,partitions, array):
        """
        @param partitions - the number of partitions to divide array into
        @param array - the array to divide
        @return an array of the partitioned array parts (array of subarrays)
        """
        nextOffset = incrOffset = len(array)/partitions
        remainder = len(array)%partitions
        lastOffset = 0
        partitionedArray = []
        
        for i in range(partitions):
            partitionedArray.append(array[lastOffset:nextOffset])
            lastOffset= nextOffset
            nextOffset += incrOffset
        
        partitionedArray[i].extend(array[incrOffset:incrOffset + remainder])
                    
        return partitionedArray
   
    def encodeData(self,trainSet,encodingMethod):
        '''
        @param trainSet -  the set of tuples structured as (textBag, rating) 
        @param encodingMethod -  a function that encodes the data
        @return: a tuple set of encoded data and rating
        '''
        
        return [(encodingMethod(tokenizedText), rating) for (tokenizedText, rating) in trainSet] 
    
    def generateLearningSetsFromReviews(self,reviews, ratings,buckets):
        '''
        produces a set of data for supervised learning into labeled buckets 
        trainSet is training data
        devSet is data used to correct algorithm
        testSet is data used to test algorithm
        @param reviewsSet -  array of ReviewContainer object
        @param ratings - array of ratings to extract reviews with 
        @param buckets - map of names to percentages to break learning data into, must sum to 1
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

        for value in learningSets.values():
            random.shuffle(value)
                            
        return learningSets