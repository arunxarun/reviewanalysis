
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

  def testCommonTermAnalysis(self):
        pageUrl = '/reviews/www.zulily.com'
        filename = './resources/zulily.pkl'
        try:
            sjr = SiteJabberReviews(pageUrl,filename)
            sjr.load()
            asd = AnalyzeSiteData()
            
            cfd = asd.generateCFD(sjr)
            
            fd1 = cfd[1]
            fd5 = cfd[5]
            
            common = [a for a in fd1.keys() if a in fd5.keys()]
            
            termFreqDiff = []
            
            for term in common:
                freq1 = fd1.freq(term)
                freq5 = fd5.freq(term)
                diff = abs(freq1 - freq5)
                termFreqDiff.append((term,diff))
                
            termFreqDiff.sort(key = itemgetter(1))
            
            maxval = termFreqDiff[0][1]
            
            normedTermFreqDiff = [(term,float(freq)/maxval) for (term, freq) in termFreqDiff]
            
        except Exception as inst:
            self.fail(inst)
            