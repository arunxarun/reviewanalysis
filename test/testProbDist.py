'''
Created on Mar 2, 2014

@author: jacoba100
'''
import unittest
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

class Test(unittest.TestCase):


    def testDefaultClassification(self):
            
            pageUrl = '/reviews/www.zulily.com'
            filename = '../test/resources/zulily.pkl'
            try:
                growthFactor = 9
                sjr = SiteJabberReviews(pageUrl,filename)
                sjr.load()
                
                badReviews = sjr.reviewsByRating[1]
                
                asd = AnalyzeSiteData()
                allBadReviewWords = []
                totalBadRevLen = 0
                
                for review in badReviews:
                    bag = asd.textBagFromRawText(review.text)
                    allBadReviewWords.extend(bag)
                    totalBadRevLen += len(bag)
               
                fdOldBad = FreqDist(allBadReviewWords) 
                badReviewCt = len(badReviews)
                avgRevLen = totalBadRevLen/badReviewCt
                
                
                # create X reviews of avgRevLen
                for i in range(growthFactor*badReviewCt):
                    rev = Review(self.createReview(allBadReviewWords,avgRevLen),"1.0")
                    sjr.addReview(rev)
                
#               
                newBadReviews= sjr.reviewsByRating[1]

                allNewBadReviewWords = []
                
                for review in newBadReviews:
                    bag = asd.textBagFromRawText(review.text)
                    allNewBadReviewWords.extend(bag)
                    
                
                fdNewBad = FreqDist(allNewBadReviewWords)
                
                allRatios = 0.0
                print 'old distribution len = %d'%len(fdOldBad.keys())
                print 'new distribution len = %d'%len(fdNewBad.keys())
                
                for word in fdOldBad.keys():
                    if fdNewBad[word] == 0:
                        print ' word not found in generated distribution: %s'%word 
                    else:
                        allRatios+= float(fdOldBad['order'])/fdNewBad['order']
                
                avg = float(allRatios)/len(fdOldBad.keys())
                
                print 'avg ratio = %.9f'%avg
                
                
                                
                
            except Exception as inst:
                self.fail(inst)
                
                
    def createReview(self,baseText,reviewLength):
        randLen = len(baseText)
        baseStr = ""
        for i in range(reviewLength):
            baseStr += (baseText[random.randint(0,randLen-1)] + ' ')
        
        return baseStr

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()