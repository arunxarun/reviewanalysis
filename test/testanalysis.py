'''
Created on Jan 16, 2014

@author: jacoba100
'''
import unittest
from sitejabberreviews import SiteJabberReviews
from analyzesitedata import AnalyzeSiteData
from operator import itemgetter
import matplotlib.pyplot as plt

from nltk.probability import FreqDist
import nltk
import random

class Test(unittest.TestCase):


#    def testDownload(self):
#        
#        pageUrl = '/reviews/www.zulily.com'
#        filename = './resources/zulily.pkl'
#        
#        try:
#            sjr = SiteJabberReviews(pageUrl,filename)
#            sjr.download(True)
#        except Exception as inst:
#            self.fail(inst)
#
#    
#    def testUpload(self):
#        pageUrl = '/reviews/www.zulily.com'
#        filename = './resources/zulily.pkl'
#        
#        try:
#            sjr = SiteJabberReviews(pageUrl,filename)
#            sjr.load()
#            
#            asd = AnalyzeSiteData()
#        
#            asd.plotReviewCounts(sjr)
#        
##            self.assertnotEqual(None,cfd,'ConditionalFreqDist should not be null when returned from AnalyzeSiteData.generate()')
##            cfd = asd.generateCFD(sjr)
#        except Exception as inst:
#            self.fail(inst)
#            
#    def testCommonTermAnalysis(self):
#        pageUrl = '/reviews/www.zulily.com'
#        filename = './resources/zulily.pkl'
#        try:
#            sjr = SiteJabberReviews(pageUrl,filename)
#            sjr.load()
#            asd = AnalyzeSiteData()
#            
#            cfd = asd.generateCFD(sjr)
#            
#            fd1 = cfd[1]
#            fd5 = cfd[5]
#            
#            common = [a for a in fd1.keys() if a in fd5.keys()]
#            
#            termFreqDiff = []
#            
#            for term in common:
#                freq1 = fd1.freq(term)
#                freq5 = fd5.freq(term)
#                diff = abs(freq1 - freq5)
#                termFreqDiff.append((term,diff))
#                
#            termFreqDiff.sort(key = itemgetter(1))
#            
#            maxval = termFreqDiff[0][1]
#            
#            normedTermFreqDiff = [(term,float(freq)/maxval) for (term, freq) in termFreqDiff]
#            
#        except Exception as inst:
#            self.fail(inst)
#            

        
        
#    def testcfdanalysis(self):
#        pageUrl = '/reviews/www.zulily.com'
#        filename = './resources/zulily.pkl'
#        try:
#            sjr = SiteJabberReviews(pageUrl,filename)
#            sjr.load()
#            asd = AnalyzeSiteData()
#            
#            cfd = asd.generateCFD(sjr)
#            
#            fd1 = cfd[1]
#            fd5 = cfd[5]
#            
#            relativeDists = []
#            for key in fd1.keys()[:200]:
#                if key in fd5.keys():
#                    val = abs(fd1.freq(key) - fd5.freq(key))
#                    relativeDists.append((key,fd1.freq(key),fd5.freq(key),val))
#            
#            relativeDists.sort(key=itemgetter(3),reverse=True)
#            
#            for (key,fd1prob,fd5prob,val) in relativeDists:
#                print "%s: fd1:%.9f fd5:%.9f val=%.9f"%(key,fd1prob,fd5prob,val)
#                    
#            
#            yvals = [val[3] for val in relativeDists]
#            
#            plt.plot(yvals)
#            plt.show() 
#        except Exception as inst:
#            self.fail(inst)
            
            
#              
#    def testDefaultClassification(self):
#     
#        
#        
#        
#        pageUrl = '/reviews/www.zulily.com'
#        filename = './resources/zulily.pkl'
#        try:
#            sjr = SiteJabberReviews(pageUrl,filename)
#            sjr.load()
#            asd = AnalyzeSiteData()
#            trainingSet1, testSet1 = asd.generateTestAndTrainingSetsFromReviews(sjr, 1, 0.8)
#            
#            self.assertEqual(len(trainingSet1), int(0.8*len(sjr.reviewsByRating[1])))
#            self.assertEqual(len(testSet1), len(sjr.reviewsByRating[1]) - len(trainingSet1))
#            
#            trainingSet5, testSet5 = asd.generateTestAndTrainingSetsFromReviews(sjr, 5, 0.8)
#            self.assertEqual(len(trainingSet5), int(0.8*len(sjr.reviewsByRating[5])))
#            self.assertEqual(len(testSet5), len(sjr.reviewsByRating[5]) - len(trainingSet5))
#            
#            
#            rawTrainingSetData = []
#            rawTrainingSetData.extend(trainingSet1)
#            rawTrainingSetData.extend(trainingSet5)
#            random.shuffle(rawTrainingSetData)
#            
#            rawTestSetData = []
#            rawTestSetData.extend(testSet1)
#            rawTestSetData.extend(testSet5)
#            random.shuffle(rawTestSetData)
#            
#            # for raw Training Data, generate all words in the data
#            all_words = [w for (words, condition) in rawTrainingSetData for w in words]
#            fdTrainingData = FreqDist(all_words)
#            # take an arbitrary subset of these
#            defaultWordSet = fdTrainingData.keys()[:100]
#            
#            def emitDefaultFeatures(tokenizedText):
#                '''
#                @param tokenizedText: an array of text features
#                @return: a feature map from that text.
#                '''
#                tokenizedTextSet = set(tokenizedText)
#                featureSet = {}
#                for text in defaultWordSet:
#                    featureSet['contains:%s'%text] = text in tokenizedTextSet
#                
#                return featureSet
#        
#            encodedTrainSet = asd.encodeData(rawTrainingSetData,emitDefaultFeatures )
#            classifier = nltk.NaiveBayesClassifier.train(encodedTrainSet)
#            
#            encodedTestSet = asd.encodeData(rawTestSetData, emitDefaultFeatures)
#            print nltk.classify.accuracy(classifier, encodedTestSet)
#            classifier.show_most_informative_features(10) 
#                
#            
#        except Exception as inst:
#            self.fail(inst)
#        
              
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
            
            dedupedBadReviewRawTerms = asd.generateLeftSideFreqDist(fd1, fd5)
#            
            uniqueTermsByRating = {}
            uniqueTermsByRating[1] = dedupedBadReviewRawTerms.keys()
            dedupedGoodReviewRawTerms = asd.generateLeftSideFreqDist(fd5,fd1)
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
                    if exclude == False: 
                        featureSet['contains:%s'%text] = text in filterSet
                    if exclude == True: 
                        featureSet['contains:%s'%text] = text not in filterSet
                
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
#            
        

#    def testIterateTowardsAccuracyMaximum(self):
#     
#        pageUrl = '/reviews/www.zulily.com'
#        filename = './resources/zulily.pkl'
#        try:
#            sjr = SiteJabberReviews(pageUrl,filename)
#            sjr.load()
#            asd = AnalyzeSiteData()
#            trainingSet1, testSet1 = asd.generateTestAndTrainingSetsFromReviews(sjr, 1, 0.8)
#            trainingSet5, testSet5 = asd.generateTestAndTrainingSetsFromReviews(sjr, 5, 0.8)
#            
#            cfd = asd.generateCFD(sjr)
#            fd1 = cfd[1]
#            fd5 = cfd[5]
#            
#            
#            dedupedBadReviewRawTerms = asd.generateLeftSideFreqDist(fd1, fd5)
##            
#            uniqueTermsByRating = {}
#            uniqueTermsByRating[1] = dedupedBadReviewRawTerms.keys()
#            dedupedGoodReviewRawTerms = asd.generateLeftSideFreqDist(fd5,fd1)
#            uniqueTermsByRating[5] = dedupedGoodReviewRawTerms.keys()
#            exclude = False
#            
#            def emitDeDupedFeatures(tokenizedText):
#                
#                filterList = uniqueTermsByRating
#                filterSet = set(filterList)
#                '''
#                expects an array of tokenized text
#                emits a feature map from that text.
#                '''
#                
#                featureSet = {}
#                
#                for text in tokenizedText:
#                    if exclude == False and text in filterSet:
#                        featureSet['contains:%s'%text] = text
#                    if exclude == True and text not in filterSet:
#                        featureSet['contains:%s'%text] = text
#                
#                return featureSet
#            
#            
#            rawTrainingSetData = []
#            rawTrainingSetData.extend(trainingSet1)
#            rawTrainingSetData.extend(trainingSet5)
#            
#            rawTestSetData = []
#            rawTestSetData.extend(testSet1)
#            rawTestSetData.extend(testSet5)
#            
#            encodedTrainSet = asd.encodeData(rawTrainingSetData,emitDeDupedFeatures)
#            classifier = nltk.NaiveBayesClassifier.train(encodedTrainSet)
#            
#            encodedTestSet = asd.encodeData(rawTestSetData,emitDeDupedFeatures)
#            
#            print nltk.classify.accuracy(classifier, encodedTestSet)
#            classifier.show_most_informative_features(5)
#              
#            
#        except Exception as inst:
#            self.fail(inst)      
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()