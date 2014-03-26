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
from nltk.probability import ConditionalFreqDist
import nltk
from nltk.corpus import stopwords

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
            
            
              
   
        
              
   
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()