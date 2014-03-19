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
from bayeshelper import BayesHelper

class Test(unittest.TestCase):


    def testDefaultClassification(self):
        pageUrl = '/reviews/www.zulily.com'
        filename = '../test/resources/zulily.pkl'
        
        sjr = SiteJabberReviews(pageUrl,filename)
        helper = BayesHelper()
        sjr.load()
        results = []
        iterations = 10
        folds = 10
        for i in range(iterations):
            partitionedBadRatings = helper.partitionArray(folds,sjr.reviewsByRating[1])
            partitionedGoodRatings = helper.partitionArray(folds,sjr.reviewsByRating[5])    
            acc = self.probDist(folds,i,{1:partitionedBadRatings,5:partitionedGoodRatings})
            results.append(acc)
            
        
        total = 0
        for x in range(len(results)):
            total+= results[x]
            
        avgResults = float(total)/iterations
        
        print "average result = %.9f"%avgResults
    
    def probDist(self,folds, iteration, reviewsByRating):    
       
        try:
            helper = BayesHelper()
            baseTraining = []
            allTest = []
            
            baseTraining,allTest = helper.buildKFoldValidationSets(folds,iteration, reviewsByRating)
            
            # with these sets, boost # of pos reviews to= num of neg reviews in training data.
            badTrainingReviews = [review for review in baseTraining if review.rating == 1]
            baseGoodTrainingReviews = [review for review in baseTraining if review.rating == 5]
            
            ratio = int(float(len(badTrainingReviews))/len(baseGoodTrainingReviews))
            
            #UNCOMMENT TO BOOST POSITIVE REVIEW DATA
            #goodTrainingReviews = helper.increaseReviewData(baseGoodTrainingReviews, 5, ratio)
            allTraining = []
            allTraining.extend(badTrainingReviews)
            #UNCOMMENT TO BOOST POSITIVE REVIEW DATA
            #allTraining.extend(goodTrainingReviews)
            #COMMMENT WHEN BOOSTING POSITIVE REVIEW DATA
            allTraining.extend(baseGoodTrainingReviews)
            
            allReviews = []
            allReviews.extend(allTraining)
            allReviews.extend(allTest)
            
            allTrainingWords = [w for review in allReviews for w in (helper.textBagFromRawText(review.text))]
            
            fdTrainingData = FreqDist(allTrainingWords)
            # take an arbitrary subset of these
            defaultWordSet = fdTrainingData.keys()[:2500]
#            
            def emitDefaultFeatures(tokenizedText):
                '''
                @param tokenizedText: an array of text features
                @return: a feature map from that text.
                '''
                tokenizedTextSet = set(tokenizedText)
                featureSet = {}
                for text in defaultWordSet:
                    featureSet['contains:%s'%text] = text in tokenizedTextSet
                
                return featureSet
            
            classifier = None  
            
            allTrainingWordRatingTuples = [(helper.textBagFromRawText(review.text), review.rating) for review in allTraining]     
             
            encodedTrainSet = helper.encodeData(allTrainingWordRatingTuples,emitDefaultFeatures )
            classifier = nltk.NaiveBayesClassifier.train(encodedTrainSet)
            
            allTestWordRatingTuples = [(helper.textBagFromRawText(review.text),review.rating) for review in allTest]
            
            encodedTestSet = helper.encodeData(allTestWordRatingTuples, emitDefaultFeatures)
            accuracy =  nltk.classify.accuracy(classifier, encodedTestSet)
            print "--------------------------------------------------------"
            
            print "test iteration %d"%iteration
            print "len all training word tuples = %d"%len(allTrainingWordRatingTuples)
            print "len all test word tuples = %d"%len(allTestWordRatingTuples)
            print "--------------------------------------------------------"
            print "accuracy = %.9f"%accuracy
            
            print "----------------------------"
            classifier.show_most_informative_features(10) 
            print "----------------------------"
            print "precision errors"
            shouldBeClassed1 = []
            shouldBeClassed5 = []
            badReviewCt = 0
            goodReviewCt = 0
            for (textbag, rating) in allTestWordRatingTuples:
                testRating = classifier.classify(emitDefaultFeatures(textbag))
                if testRating != rating:
                    if rating == 1:
                        shouldBeClassed1.append(textbag)
                    else:
                        shouldBeClassed5.append(textbag)
                if rating == 1:
                    badReviewCt += 1
                elif rating == 5:
                    goodReviewCt += 1
                
            
            print "total 1 star reviews in test = %d"%badReviewCt             
            print "length of mis-classified 1 star reviews = %d"%len(shouldBeClassed1)            
            print "total 5 star reviews in test = %d"%goodReviewCt
            print "length of mis-classified 5 star reviews = %d"%len(shouldBeClassed5)
            
            print "training data size = %d"%len(allTraining)
            print "test data size = %d"%len(allTest)
            
        
            return accuracy
        except Exception as inst:
            self.fail(inst)
     
     
                
    
    
    
    
    
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()