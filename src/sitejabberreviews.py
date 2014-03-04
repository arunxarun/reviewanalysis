'''
Created on Jan 2, 2014

@author: jacoba100
'''

from bs4 import BeautifulSoup
import urllib2
import re
import pickle
import re
#from nltk.book import FreqDist
#from nltk.corpus import stopwords
import pickle
from review import Review
from review import ReviewContainer
import matplotlib.pyplot as plt
    
class SiteJabberReviews(ReviewContainer):
    
    def __init__(self,pageUrl,filename):
        super(SiteJabberReviews,self).__init__("http://www.sitejabber.com",pageUrl,filename)
        
    def download(self, save=True):
        '''
        downloads all reviews of a specific site from sitejabber.com
        NOTE navigation logic is specific to sitejabber.com
        ''' 
        # first get the pages we need to navigate to to get all reviews for this site. 
        page = urllib2.urlopen(self.pageUrl)
        soup = BeautifulSoup(page)
        
        pageNumDiv = soup.find('div',{'class':'page_numbers'})
        
        anchors = pageNumDiv.find_all('a')
        
        urlList = []
        urlList.append(self.pageUrl)
        for anchor in anchors:
            urlList.append(self.base + anchor['href'])
        
        # with all pages set, pull each page down and extract review text and rating. s
        for url in urlList:    
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
            divs = soup.find_all('div',id=re.compile('ReviewRow-.*'))
            
                    
            for div in divs:
                text = div.find('p',id=re.compile('ReviewText-.*')).text
                rawRating = div.find(itemprop='ratingValue')['content']
                
                
                r = Review(text,rawRating)
                
                reviews = self.reviewsByRating[r.rating]
                reviews.append(r)
        
        if save == True:
            self.saveToDisk()
            
            
        return self.reviewsByRating
            
    
    
            
if __name__ == '__main__':
    
    
    #pageUrl = 'reviews/www.zulily.com'
    #filename = "/Users/jacoba100/data/reviews/zulilyreviews.pkl"
    pageUrl = 'reviews/www.zappos.com'
    filename = "zapposreviews.pkl"
    
    sjr = SiteJabberReviews(pageUrl,filename)
    
    reviewsByRating = sjr.download(True)
    
    #reviewsByRating = sjr.load()
     
    #---------------port velow this line----------------#        
    sortedRatings = sorted(reviewsByRating.keys())
    
    
    
    for rating in sortedRatings:
        textBag = []
        print "rawRating = %d"%rating
        print "review count = %d"%len(reviewsByRating[rating])
    xvals = [x for x in reviewsByRating.keys()]
    yvals = [len(reviewsByRating[key]) for key in reviewsByRating.keys()]
    
    plt.plot(xvals,yvals)
    plt.show()
    

        # build up all words in text.
        
#        for reviews in reviewsByRating[rating]:
#            rawText = reviews.text
#            sentences = rawText.split('.')
#            for sentence in sentences:
#                parts = sentence.split()
#                textBag.extend(parts)
#                
        
    
#        cleanedTextBag = [w for w in textBag if w not in stopwords.words('english')]
#        
#        cleanFd = FreqDist(cleanedTextBag)
#        
#        print cleanFd.keys()[:20]
        
            
        
    