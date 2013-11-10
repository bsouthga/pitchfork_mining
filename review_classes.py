# Classes for review scraping
# Also includes a function for writing the data to .tsv
# Ben Southgate
# 10/19/13


########################
# Pitchfork Review Class
########################


class browser_opener(FancyURLopener):
    version =  'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) \
                Gecko/20071127 Firefox/2.0.0.11'



########################
# Pitchfork Review Class
########################


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

        super(Review, self).__init__()        
        
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

    # Easy Accessor
    def get(self):

        return  [   self.artist,   
                    self.album,    
                    self.label,    
                    self.date,     
                    self.score,    
                    self.author,   
                    self.color_avg,
                    self.imglink,
                    self.reviewlink,    
                    self.special,
                    self.editorial
                    ]  


########################
# Metacritic Classes
########################


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


########################
# Helper Functions
########################


def progress_bar(total, current, text = ""):
    '''
    Shnazzy Progress Bar
    '''
    sys.stdout.write('\r')

    sys.stdout.write(text + ' {0:.0f}% complete'.format(
                                                    float(current*100) / total)
                                                    )
    
    sys.stdout.flush()


# Function for writing dictionary of Review objects to .tsv
def write_data(review_dict, outname):
    '''
        Write data to .tsv file, parameters are a dictionary of review
        objects, along with a filename for the .tsv

    '''
    
    with open(outname, 'w') as out:

        headers = [ "artist", 
                    "album",
                    "label", 
                    "date", 
                    "score", 
                    "author", 
                    "color_avg",
                    "imglink",
                    "reviewlink",
                    "special",
                    "editorial"
                    ]

        out.write( "\t".join(headers) + "\n")
        
        for key in review_dict.keys():
            review = review_dict[key]
            out.write( "\t".join( [str(x) for x in review.get()]) + "\n")

