'''
Created on Jan 16, 2014

@author: jacoba100
'''
import unittest
from sitejabberreviews import SiteJabberReviews
from analyzesitedata import AnalyzeSiteData
import nltk
import random

class Test(unittest.TestCase):


    def testDownload(self):
        
        pageUrl = '/reviews/www.zulily.com'
        filename = './resources/zulily.pkl'
        
        try:
            sjr = SiteJabberReviews(pageUrl,filename)
            sjr.download(True)
        except Exception as inst:
            self.fail(inst)

    
    def testUpload(self):
        pageUrl = '/reviews/www.zulily.com'
        filename = './resources/zulily.pkl'
        
        try:
            sjr = SiteJabberReviews(pageUrl,filename)
            sjr.load()
            
            asd = AnalyzeSiteData()
        
            asd.plotReviewCounts(sjr)
        
#            self.assertnotEqual(None,cfd,'ConditionalFreqDist should not be null when returned from AnalyzeSiteData.generate()')
#            cfd = asd.generateCFD(sjr)
        except Exception as inst:
            self.fail(inst)
            
    
    def testDefaultClassification(self):
     
        def emitDefaultFeatures(tokenizedText):
            '''
            @param tokenizedText: an array of text features
            @return: a feature map from that text.
            '''
            
            featureSet = {}
            for text in tokenizedText:
                featureSet['contains:%s'%text] = text
            
            return featureSet
        
        pageUrl = '/reviews/www.zulily.com'
        filename = './resources/zulily.pkl'
        try:
            sjr = SiteJabberReviews(pageUrl,filename)
            sjr.load()
            asd = AnalyzeSiteData()
            trainingSet1, testSet1 = asd.generateTestAndTrainingSetsFromReviews(sjr, 1, 0.8)
            
            self.assertEqual(len(trainingSet1), int(0.8*len(sjr.reviewsByRating[1])))
            self.assertEqual(len(testSet1), len(sjr.reviewsByRating[1]) - len(trainingSet1))
            
            trainingSet5, testSet5 = asd.generateTestAndTrainingSetsFromReviews(sjr, 5, 0.8)
            self.assertEqual(len(trainingSet5), int(0.8*len(sjr.reviewsByRating[5])))
            self.assertEqual(len(testSet5), len(sjr.reviewsByRating[5]) - len(trainingSet5))
            
            
            rawTrainingSetData = []
            rawTrainingSetData.extend(trainingSet1)
            rawTrainingSetData.extend(trainingSet5)
            random.shuffle(rawTrainingSetData)
            
            rawTestSetData = []
            rawTestSetData.extend(testSet1)
            rawTestSetData.extend(testSet5)
            random.shuffle(rawTestSetData)
            
            encodedTrainSet = asd.encodeData(rawTrainingSetData,emitDefaultFeatures )
            classifier = nltk.NaiveBayesClassifier.train(encodedTrainSet)
            
            encodedTestSet = asd.encodeData(rawTestSetData, emitDefaultFeatures)
            print nltk.classify.accuracy(classifier, encodedTestSet)
            classifier.show_most_informative_features(5) 
                
            
        except Exception as inst:
            self.fail(inst)
        
              
    def testRemoveCommonTermsClassification(self):
     
        pageUrl = '/reviews/www.zulily.com'
        filename = './resources/zulily.pkl'
        try:
            sjr = SiteJabberReviews(pageUrl,filename)
            sjr.load()
            asd = AnalyzeSiteData()
            trainingSet1, testSet1 = asd.generateTestAndTrainingSetsFromReviews(sjr, 1, 0.8)
            trainingSet5, testSet5 = asd.generateTestAndTrainingSetsFromReviews(sjr, 5, 0.8)
            
            cfd = asd.generateCFD(sjr)
            fd1 = cfd[1]
            fd5 = cfd[5]
            
            dedupedBadReviewRawTerms = asd.generateLeftJoinFreqDist(fd1, fd5)
#            
            uniqueTermsByRating = {}
            uniqueTermsByRating[1] = dedupedBadReviewRawTerms.keys()
            dedupedGoodReviewRawTerms = asd.generateLeftJoinFreqDist(fd5,fd1)
            uniqueTermsByRating[5] = dedupedGoodReviewRawTerms.keys()
            exclude = False
            
            def emitDeDupedFeatures(tokenizedText):
                
                filterList = uniqueTermsByRating
                filterSet = set(filterList)
                '''
                expects an array of tokenized text
                emits a feature map from that text.
                '''
                
                featureSet = {}
                
                for text in tokenizedText:
                    if exclude == False and text in filterSet:
                        featureSet['contains:%s'%text] = text
                    if exclude == True and text not in filterSet:
                        featureSet['contains:%s'%text] = text
                
                return featureSet
            
            
            rawTrainingSetData = []
            rawTrainingSetData.extend(trainingSet1)
            rawTrainingSetData.extend(trainingSet5)
            
            rawTestSetData = []
            rawTestSetData.extend(testSet1)
            rawTestSetData.extend(testSet5)
            
            encodedTrainSet = asd.encodeData(rawTrainingSetData,emitDeDupedFeatures)
            classifier = nltk.NaiveBayesClassifier.train(encodedTrainSet)
            
            encodedTestSet = asd.encodeData(rawTestSetData,emitDeDupedFeatures)
            
            print nltk.classify.accuracy(classifier, encodedTestSet)
            classifier.show_most_informative_features(5)
              
            
        except Exception as inst:
            self.fail(inst)            
            
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()