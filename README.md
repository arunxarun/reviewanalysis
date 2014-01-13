reviewanalysis
==============

sample code from blog post: http://arunxjacob.blogspot.com/2014/01/making-sense-of-unstructured-text-in.html.
Code I wrote to download, save, and analyze text from online review sites.

Right now the only site I'm scraping from is SiteJabber (http://sitejabber.com)

## Requirements: 

nltk
matplotlib
pickle
beautifulsoup


## Samples:
### To get text data: 

  pageUrl = 'reviews/www.zappos.com'
  filename = "zapposreviews.pkl"
    
  sjr = SiteJabberReviews(pageUrl,filename)
    
  reviewsByRating = sjr.download(True)

### To load that data from file: 

  sjr = SiteJabberReviews(pageUrls[i],filenames[i])
  sjr.load()
  
### To plot ratings by review:

  asd = AnalyzeSiteData()
        
  asd.plotReviews(sjr)

### To build an nltk ConditionalFreqDist:

  cfd = asd.generateCFD(sjr)
  
  
  
## Classes: 

* Review -- holds review text and rating
* ReviewContainer -- contains a map of ratings that hold lists of reviews, and the logic for saving it to/loading it from disk. Contains a method stub to download the data that throws an exception because that method should be implemented in subclasses.
* AnalyzeSiteData -- contains methods that use the ratings->reviews map to generate plots, ConditionalFrequencyDistributions, etc. 
* SiteJabberReviews -- a subclass of ReviewContainer that has download logic specific to http://sitejabber.com


  
  
