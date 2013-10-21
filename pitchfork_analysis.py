# Pitchfork Review Analysis
# Ben Southgate
# 10/19/13

# Must import review class from pitchfork_reviews.py
import shelve
from pitchfork_reviews import Review
import time

def yearly_color(full_data, score_buckets):
    '''
        Calculates album artwork color averages for a buckets of 
        a numeric variable, like score, review date, or album release year 
    '''

    # Dictionary to hold color averages for reviews in score buckets
    score_dict = {bucket:[] for bucket in score_buckets}

    # Build list of average colors in each bucket
    for key in full_data.keys():
        review = full_data[key]
        year = int(review.date.split(",")[1])
        for bucket in score_buckets:
            if review.date != "None" and review.color_avg != "None":
                if year == bucket:
                    score_dict[bucket].append(review.color_avg)

    # Contianer dictionary
    color_averages = {}

    # Average color values in bucket
    for bucket in sorted(score_dict.keys()):
        color_list = score_dict[bucket]
        rgb = [0,0,0]
        for color in color_list:
            for i in range(3):
                rgb[i] += float(color[i]) / len(color_list)

        for i in range(3):
            rgb[i] = int(rgb[i])

        color_averages[bucket] = rgb

    return color_averages
    

def main():

    # # Tuple Score Buckets
    # score_buckets = [x for x in range(1999,2014)]

    # analysis = yearly_color(full_data, score_buckets)

    # for key in sorted(analysis.keys()):
    #     print(analysis[key])


if __name__ == "__main__":
    main()
