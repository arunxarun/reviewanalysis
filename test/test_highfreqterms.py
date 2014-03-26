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
            
#            commonDist = [freqDiff for (a,b,c,freqDiff) in commonTermFreqs]
#            
#            plt.plot(commonDist)
#            plt.show()
            
            # keep an arbitrary number
            
            filterTerms = [w for (w,a,b,freq) in commonTermFreqs if freq > 0.001]
            
            # add non common terms (note that bayesian will smooth zero terms out)
            print 'high frequency differential featureset'
            fd1Only = [w for w in fd1.keys() if w not in fd5.keys()]
            filterTerms.extend(fd1Only)
            fd5Only = [w for w in fd5.keys() if w not in fd1.keys()]
            filterTerms.extend(fd5Only)
            defaultWordSet = set(filterTerms)
            
      
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
                   
                   
#            incorrectText1 = [(-1,w) for bag in shouldBeClassed1
#                        for w in bag if w not in stopwords.words('english')]
#            
#            correctText1 = [(1,w) for bag in buckets['training']
#                        for w in bag if w not in stopwords.words('english')]
#            
#            allText1 = []
#            allText1.extend(incorrectText1)
#            allText1.extend(correctText1)
#            
#            cfdText1 = ConditionalFreqDist(allText1)
#            
#            
#            incorrectText5 = [(-5,w) for bag in shouldBeClassed5
#                        for w in bag if w not in stopwords.words('english')]
#            
#            
#            correctText5 = [(5,w) for (bag, rating) in buckets['training']
#                        for w in bag if rating == 5 and w not in stopwords.words('english')]
#            
#            
#            allText5 = []
#            allText5.extend(incorrectText5)
#            allText5.extend(correctText5)
#            
#            cfdText5 = ConditionalFreqDist(allText5)
            
             
            return accuracy
        
        except Exception as inst:
            self.fail(inst)
                

            
    def testRemoveLowFreqDiffClassification(self):
     
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
                        
            commonTerms = [w for w in fd1.keys() if w in fd5.keys()]
            fd1Len = len(fd1.keys())
            fd5Len = len(fd5.keys())
            
            TermsAndFreqs = [(w, abs((float(fd1.frequency(w))/fd1Len) - (float(fd5.frequency(w))/fd5Len))) for w in commonTerms]
            # this gives common terms, but we need to splice in 'uncommon' terms as well. 
            # in fact, splice them in 'first', try the classification, and see what happens when you add in a subset of features. 
            
            TermsAndFreqs.sort(key = itemgetter(1),reverse=True)
            
            
            
            
            
            
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
        

    def testIterateTowardsAccuracyMaximum(self):
     
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