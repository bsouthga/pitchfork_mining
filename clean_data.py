# Pitchfork Data Cleaning
# Ben Southgate
# 10/19/13

# Must import review class from pitchfork_reviews.py
import shelve, time
from pitchfork_reviews import Review
from pitchfork_reviews import Artist


def clean_time(full_data):
    '''
        Convert data/time string into time.struct_time objects
    '''

    for key in full_data.keys():
        review = full_data[key]
        date = review.date
        newdate = time.strptime(date.replace(",","")," %B %d %Y ")
        review.time = newdate
        full_data[key] = review

    return full_data


def assign_albums_artist(full_data):
    '''
        Find artists with sequential album reviews. Creates an artist object,
        itself containing all the reviews.

        For multi-artist albums, all artists are given the review
    '''
    
    artist_dict = {}

    for key in full_data.keys():

        review = full_data[key]

        artist = review.artist

        # Check to see if more than one artist is in the name
        if " & " or " / " in artist:



def main():
    # Draw data from object storage
    storage = shelve.open('Pitchfork_data_full')
    full_data = storage['data']

    cleaned_time = clean_time(full_data)

    storage['cleaned data'] = cleaned_time
    storage.close()

if __name__ == "__main__":
    main()
