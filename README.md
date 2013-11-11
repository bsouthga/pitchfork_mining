Mining with Pitchfork
=====================

This is a little project to see the if there are any patterns to the reviews that [Pitchfork](http://pitchfork.com) has written over the years. Specifically, I intend to investigate the "Sophomore Slump" -- the percieved reduction in score a band recieves for their second album. [Metacritic](http://metacritic.com) data is also utilized to investigate any systematic bias in any direction relative to other known critics.

Web Scraping Data Structures
-----------------------

In order to store the many components of each review, several data structures were created to ease storage and collection. For collecting information on pitchfork, a single class was used. As each Metacritic album has multiple reviews from varying critics, a two part class structure was utilized.

### Pitchfork Review "Scrapings":

```python

class PitchforkReview(object):
    ''' Store a single Pitchfork Review '''
    def __init__(   self, 
                    artist, 
                    album,
                    label, 
                    date, 
                    score, 
                    author, 
                    color_avg,
                    imglink,
                    reviewlink,
                    special,
                    editorial
                    ):

        super(PitchforkReview, self).__init__()        
        
        self.artist     = artist # Musical artist
        self.album      = album 
        self.label      = label # Record label producing album
        self.date       = date # Review date
        self.score      = score 
        self.author     = author # Review author
        self.color_avg  = color_avg  # Average color of album cover
        self.imglink    = imglink # Link to image of album cover
        self.reviewlink = reviewlink # Link to review page
        self.special    = special    # Win best new music etc?
        self.editorial  = editorial # Full text of review
```

### Metacritic Review "Scrapings":

```python

class MetaItem(object):
    ''' Stores all the different reviews for this item.'''
    def __init__(   self,
                    title,
                    artist_name,
                    meta_score,
                    user_average,
                    release_date
                    ):

        super(MetaItem, self).__init__()

        self.title = title
        self.artist = artist_name
        self.meta_score = meta_score
        self.user_average = user_average
        self.release_date = release_date
        self.reviews = {}

    def add_review(self, review):
        ''' add critic reviews '''
        self.reviews[review.critic] = review


class MetaReview(object):
    ''' A single review for storage in an item object '''
    def __init__(   self,
                    critic,
                    score,
                    text,
                    link
                    ):

        super(MetaReview, self).__init__()

        self.critic = critic # Name of publication reviewing album
        self.score = score # Score from above critic
        self.text = text # Snipit of review text
        self.link = link # Link to review page (off MetaCritic)
```

