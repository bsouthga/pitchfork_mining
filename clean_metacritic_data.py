# Reshape Metacritic Data
# Ben Southgate
# 11/03/13
 
import sys, shelve, re
from metaminer import MetaItem
from metaminer import MetaReview

reload(sys) 
sys.setdefaultencoding("utf-8")

raw_data = shelve.open('raw_data')["raw_data"]

# Remove dates from some critic names, build set of critics
critic_set = set()
pattern = re.compile('[A-Z][a-z][a-z] +[0-9]+, [0-9][0-9][0-9][0-9]')
cleaned_data = {}
for key in raw_data.keys():
    item = raw_data[key]
    for review_key in item.reviews.keys():
        review = item.reviews[review_key]
        cleaned = pattern.sub("", review.critic)
        review.critic = cleaned
        item.reviews[review_key] = review
        critic_set.add(cleaned)
    cleaned_data[key] = item


with open("metacritic_data.tsv", 'w') as out:

    out.write("\t".join([   "album",
                            "artist",
                            "meta_score",
                            "release_date"] + 
                            sorted(critic_set)) + "\n"
                            )

    for key, item in cleaned_data.iteritems():
        
        # Write a review to a row, filling in missing critics with "NA"
        out.write("\t".join([str(x) for x in
                                [  item.title, 
                                    " ".join(item.artist),
                                    item.meta_score,
                                    " ".join(item.release_date)
                                    ] + [   item.reviews[c].score 
                                            if c in item.reviews.keys() 
                                            else "NA" 
                                            for c in sorted(critic_set) 
                                            ]
                             ]
                            ) + "\n"
                    )




