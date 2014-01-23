'''
Created on Jan 20, 2014

@author: jacoba100
'''
import unittest
from sitejabberreviews import SiteJabberReviews

class Test(unittest.TestCase):


    def testDownload(self):
        # TODO: download zappos reviews and someone elses one star reviews, munge to a training set, and test
            #http://www.sitejabber.com/reviews/www.ideeli.com  
        pageUrl = '/reviews/www.ideeli.com'
        filename = './resources/ideeli.pkl'
        
        sjr = SiteJabberReviews(pageUrl,filename)
        sjr.download(True)
    
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()