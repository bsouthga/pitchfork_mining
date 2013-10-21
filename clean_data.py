# Pitchfork Data Cleaning
# Ben Southgate
# 10/19/13

# Must import review class from pitchfork_reviews.py
import shelve, time
from pitchfork_reviews import *


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

        band_name = review.artist

        # Check to see if more than one artist is in the name
        if (" & " or " / ") in band_name:

            if " & " in band_name:
                band_names = band_name.split(" & ")
            else:
                band_names = band_name.split(" / ")
            
            for name in band_names:

                cleaned = name.replace(" ", "")

                try:
                    band_object = artist_dict[cleaned]
                    band_object.add_review(review)
                    artist_dict[cleaned] = band_object

                except(KeyError):
                    band_object = Artist(name)
                    band_object.add_review(review)
                    artist_dict[cleaned] = band_object

        else:

            cleaned = band_name.replace(" ", "")

            try:
                band_object = artist_dict[cleaned]
                band_object.add_review(review)
                artist_dict[cleaned] = band_object

            except(KeyError):
                band_object = Artist(band_name)
                band_object.add_review(review)
                artist_dict[cleaned] = band_object

    return artist_dict


            



def main():


    storage = shelve.open('Pitchfork_data_full')
    full_data = storage['data']

    cleaned_time = clean_time(full_data)
    artist_data = assign_albums_artist(cleaned_time)

    storage['cleaned data'] = cleaned_time
    storage['artists'] = cleaned_time

    storage.close()



if __name__ == "__main__":
    main()
