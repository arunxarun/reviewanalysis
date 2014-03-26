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

class Test(unittest.TestCase):


    def testcfdanalysis(self):
        pageUrl = '/reviews/www.zulily.com'
        filename = './resources/zulily.pkl'
        try:
            sjr = SiteJabberReviews(pageUrl,filename)
            sjr.load()
            asd = AnalyzeSiteData()
            
            cfd = asd.generateCFD(sjr)
            
            fd1 = cfd[1]
            fd5 = cfd[5]
            
            relativeDists = []
            for key in fd1.keys()[:200]:
                if key in fd5.keys():
                    val = abs(fd1.freq(key) - fd5.freq(key))
                    relativeDists.append((key,fd1.freq(key),fd5.freq(key),val))
            
            relativeDists.sort(key=itemgetter(3),reverse=True)
            
            for (key,fd1prob,fd5prob,val) in relativeDists:
                print "%s: fd1:%.9f fd5:%.9f val=%.9f"%(key,fd1prob,fd5prob,val)
                    
            
            yvals = [val[3] for val in relativeDists]
            
            plt.plot(yvals)
            plt.show() 
        except Exception as inst:
            self.fail(inst)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()