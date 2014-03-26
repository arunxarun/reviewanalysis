reviewanalysis
==============

Code written for blog posts exploring sentiment analysis with NLTK Bayesian classsifier. 

Consists of a review site scraper -- right now the only site I'm scraping from is SiteJabber (http://sitejabber.com), and helper classes that facilitate training, testing, and evaluating classifiers.  

the training and testing is done in the unit tests specified below, see ./test directory.

## Train/Test code

### testdefaulttraining.py

this is the default training scenario, where the top 2500 terms across positive and negative reviews are used to help train the classifier.

### test_highfreqterms.py

this is an alternate approach taken where only high frequency terms were used to train the classifier.

### testprobdist.py

this approach boosted positive review frequency to help the classifer perform better on positive reviews during testing. 
 

## Requirements: 

nltk
matplotlib
pickle
beautifulsoup


## Code snippets:
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


  
  
