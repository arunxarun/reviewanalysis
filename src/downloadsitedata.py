'''
Created on Jan 4, 2014

@author: jacoba100
'''
from sitejabberreviews import SiteJabberReviews

if __name__ == '__main__':
    pageUrls = ['/reviews/www.zulily.com','/reviews/www.zappos.com']
    filenames = ['/Users/jacoba100/data/reviews/zulily.pkl','/Users/jacoba100/data/reviews/zappos.pkl']
    
    
    for i in range(len(pageUrls)):
        sjr = SiteJabberReviews(pageUrls[i],filenames[i])
        sjr.download(True)
    
    