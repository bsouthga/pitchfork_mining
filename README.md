Mining with Pitchfork
=====================

This is a little project to see the if there are any patterns to the reviews that [Pitchfork](http://pitchfork.com) has written over the years. Specifically, I intend to investigate the "Sophomore Slump" -- the percieved reduction in score a band recieves for their second album. [Metacritic](http://metacritic.com) data is also utilized to investigate any systematic bias in any direction relative to other known critics.

Review Data Structures
-----------------------

### Pitchfork Review "Scrapings":

    class PitchforkReview(object):

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
            
            self.artist     = artist
            self.album      = album
            self.label      = label
            self.date       = date
            self.score      = score
            self.author     = author
            self.color_avg  = color_avg  # average color of album cover
            self.imglink    = imglink
            self.reviewlink = reviewlink
            self.special    = special    # Win best new music etc?
            self.editorial  = editorial


### MetaCritic Review "Scrapings":

    class MetaItem(object):
        """ Stores all the different reviews for this item."""
        def __init__(self, title, artist_name, meta_score, user_average, release_date):
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
        """ A single review for storage in an item object """

        def __init__(self, critic, score, text, link):
            super(MetaReview, self).__init__()
            self.critic = critic
            self.score = score
            self.text = text
            self.link = link


