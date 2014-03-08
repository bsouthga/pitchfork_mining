# Reshape Metacritic Data
# Ben Southgate
# 11/03/13
 
import sys, shelve, re
from review_classes import MetaItem
from review_classes import MetaReview

reload(sys) 
sys.setdefaultencoding("utf-8")

raw_data = shelve.open('raw_data')["raw_data"]

# Remove dates from some critic names, build set of critics
critic_set = set()
date_regex = re.compile('[A-Z][a-z][a-z] +[0-9]+, [0-9][0-9][0-9][0-9]')
cleaned_data = {}
for key in raw_data.keys():
    item = raw_data[key]
    for review_key in item.reviews.keys():
        review = item.reviews[review_key]
        cleaned = date_regex.sub("", review.critic)
        review.critic = cleaned
        item.reviews[review_key] = review
        critic_set.add(cleaned)
    cleaned_data[key] = item


with open("metacritic_data.tsv", 'w') as out:

    out.write("\t".join([   "album",
                            "artist",
                            "meta_score",
                            "release_date",
                            "pitchfork_link"] + 
                            sorted(critic_set)) + "\n"
                            )

    for key, item in cleaned_data.iteritems():

        # Write a review to a row, filling in missing info with "NA"
        observation = [
            str(x) for x in
                [   item.title, 
                    " ".join(item.artist),
                    item.meta_score,
                    " ".join(item.release_date),
                    item.reviews["Pitchfork"].link if "Pitchfork" in item.reviews.keys() else "NA"
                    ] + [   item.reviews[c].score 
                            if c in item.reviews.keys() 
                            else "NA" 
                            for c in sorted(critic_set) 
                            ]
        ]
    
        out.write("\t".join(observation) + "\n")




