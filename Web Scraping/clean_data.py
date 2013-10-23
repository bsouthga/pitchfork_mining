# Pitchfork Data Cleaning
# Ben Southgate
# 10/19/13

# Must import review class from pitchfork_reviews.py
import shelve, time, os, sys
import pandas as pd
from pitchfork_reviews import Review
from pitchfork_reviews import progress_bar

# Convert date string to time object
def clean_time(full_data):
    '''
        Convert data/time string into time.struct_time objects
    '''
    cleaned = {}
    count = 1
    for key in full_data.keys():

        progress_bar(len(full_data.keys()),count,"Time Cleaning")
        count+=1
        review = full_data[key]
        date = review.date
        newdate = time.strptime(date.replace(",","")," %B %d %Y ")
        review.date = newdate
        cleaned[key] = review
    
    print("")
    return cleaned



def model_prep(cleaned_data):
    '''
        Construct Pandas Data Frame

        Currently only includes albums with 1 artist
    '''

    # Series for pandas data frame
    d = {   "artist"           : [] ,
            "album"            : [] ,
            "label"            : [] ,
            "author"           : [] ,
            "score"            : [] ,
            "red"              : [] ,
            "green"            : [] ,
            "blue"             : [] ,
            "year"             : [] ,
            "month"            : [] ,
            "day_of_week"      : [] ,
            "best_new_mus"     : [] ,
            "best_new_reiss"   : [] 
            }

    count = 1
    for key in sorted(cleaned_data.keys()):

        progress_bar(len(cleaned_data.keys()),count,"Data Frame Construction")
        count+=1
        
        review = cleaned_data[key]

        # Indicate more than one artist in the album
        if (" & " and " / ") not in review.artist:

            d["artist"].append(review.artist)       
            d["album"].append(review.album)        
            d["label"].append(review.label.split(";")[0])
            d["author"].append(review.author.replace("by","",1))       
            d["score"].append(review.score)        
            d["red"].append(review.color_avg[0])          
            d["green"].append(review.color_avg[1])        
            d["blue"].append(review.color_avg[2])         
            d["year"].append(review.date.tm_year)         
            d["month"].append(review.date.tm_mon)        
            d["day_of_week"].append(review.date.tm_wday) 

            if review.special == " Best New Music ":
                d["best_new_mus"].append(1)
            else:
                d["best_new_mus"].append(0)

            if review.special == " Best New Reissue ":
                d["best_new_reiss"].append(1)
            else:
                d["best_new_reiss"].append(0)

    print("")
    return pd.DataFrame(d)


def main():

    path = "/Users/Ben/Dropbox/projects/pitchfork/Data/"
    print("Importing Uncleaned Data...")

    # Open raw data from scrape
    uncleaned = shelve.open(os.path.join(path,'Uncleaned'))
    full_data = uncleaned['data']
    uncleaned.close()

    # Cleaning operations
    cleaned_time = clean_time(full_data)
    data_frame = model_prep(cleaned_time)

    print("Storing Cleaned Data...")

    # Store cleaned data   
    storage = shelve.open(os.path.join(path,'Pitchfork_Data_Shelf'))
    storage['cleaned data'] = cleaned_time
    storage['data frame']   = data_frame
    storage.close()


if __name__ == "__main__":
    main()
