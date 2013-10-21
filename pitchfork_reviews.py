# Classes for review scraping and analysis
# Also includes a function for writing the data to .tsv
# Ben Southgate
# 10/19/13

# Time class for date
from time import struct_time

# Class to contain info on one review of an album
class Review:

    def __init__(   self, 
                    artist, 
                    album,
                    label, 
                    date, 
                    score, 
                    author, 
                    color_avg,
                    imglink,
                    special,
                    editorial
                    ):        
        
        self.artist     = artist
        self.album      = album
        self.label      = label
        self.date       = date
        self.score      = score
        self.author     = author
        self.color_avg  = color_avg  # average color of album cover
        self.imglink    = imglink
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
                    self.special,
                    self.editorial
                    ]  


# Class for single artist, with multiple reviews
class Artist: 

    def __init__(   self,
                    name
                    ):      

        self.name = name
        self.reviews = {}


    def add_review(review):

        self.reviews[review.date] = review


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
                    "special",
                    "editorial"
                    ]

        out.write( "\t".join(headers) + "\n")
        
        for key in review_dict.keys():
            review = review_dict[key]
            out.write( "\t".join( [str(x) for x in review.get()]) + "\n")

