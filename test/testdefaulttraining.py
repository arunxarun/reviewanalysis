'''
Created on Mar 2, 2014

@author: jacoba100
'''

import unittest

from sitejabberreviews import SiteJabberReviews
from analyzesitedata import AnalyzeSiteData
from operator import itemgetter
import matplotlib.pyplot as plt

from nltk.probability import FreqDist
from nltk.probability import ConditionalFreqDist
import nltk
from nltk.corpus import stopwords
from bayeshelper import BayesHelper

class Test(unittest.TestCase):


    def testDefaultClassification(self):
        iteration = 10
        totalAccuracy = 0.0
        
        for i in range(iteration):
            totalAccuracy += (self.runTest(i+1))
        
        avgAccuracy = totalAccuracy/iteration
        print 'avg accuracy = %.9f'%avgAccuracy
        
        
    def runTest(self,iteration):
        print "running test %d"%iteration
        
        pageUrl = '/reviews/www.zulily.com'
        filename = '../test/resources/zulily.pkl'
        try:
            sjr = SiteJabberReviews(pageUrl,filename)
            sjr.load()
            helper = BayesHelper()
            buckets = helper.generateLearningSetsFromReviews([sjr],[1,5],{'training': 0.8,'test':0.2})
            
            self.assertEqual(len(buckets['training']), int(0.8*len(sjr.reviewsByRating[1])+int(0.8*len(sjr.reviewsByRating[5]))))
            self.assertEqual(len(buckets['test']), int(0.2*len(sjr.reviewsByRating[1])+int(0.2*len(sjr.reviewsByRating[5]))))
            
            
            
            #  generate (term) tuples for FD -- this means we need to bust out like terms from combined distributions
            
            allWords1 = [w for (textBag,rating) in buckets['training'] for w in textBag if rating == 1]
            fd1 = FreqDist(allWords1)
            
            allWords5 = [w for (textBag,rating) in buckets['training'] for w in textBag if rating == 5]
            fd5 = FreqDist(allWords5)
            
            commonTerms = [w for w in fd1.keys() if w in fd5.keys()]
            
            commonTermFreqs = [(w,fd1.freq(w), fd5.freq(w), abs(fd1.freq(w) - fd5.freq(w))) for w in commonTerms]
            
            commonTermFreqs.sort(key = itemgetter(3),reverse=True)
            

            all_words = []
            all_words.extend(allWords1)
            all_words.extend(allWords5)

            fdTrainingData = FreqDist(all_words)
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
            encodedTrainSet = helper.encodeData(buckets['training'],emitDefaultFeatures )
            classifier = nltk.NaiveBayesClassifier.train(encodedTrainSet)
            
            encodedTestSet = helper.encodeData(buckets['test'], emitDefaultFeatures)
            accuracy =  nltk.classify.accuracy(classifier, encodedTestSet)
            print "accuracy = %.9f"%accuracy
            
            classifier.show_most_informative_features(10) 
            
            shouldBeClassed1 = []
            shouldBeClassed5 = []
            
            for (textbag, rating) in buckets['test']:
                testRating = classifier.classify(emitDefaultFeatures(textbag))
                if testRating != rating:
                    if rating == 1:
                        shouldBeClassed1.append(textbag)
                    else:
                        shouldBeClassed5.append(textbag)
                        
            print "length of mis-classified 1 star reviews = %d"%len(shouldBeClassed1)            
            print "length of mis-classified 5 star reviews = %d"%len(shouldBeClassed5)
            
            print "length of all 1 star reviews submitted = %d"%len(sjr.reviewsByRating[1])
            print "length of all 5 star reviews submitted = %d"%len(sjr.reviewsByRating[5]) 
            
            print "length of test data for 1 star reviews = %d"%int(0.2*len(sjr.reviewsByRating[1]))
            print "length of test data for 5 star reviews = %d"%int(0.2*len(sjr.reviewsByRating[5]))
                   
             
            return accuracy
        
        except Exception as inst:
            self.fail(inst)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()