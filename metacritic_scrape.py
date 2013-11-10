# Metacritic Web Scraping Script
# Ben Southgate
# 10/31/13

import sys, shelve
from bs4 import BeautifulSoup as BS
from urllib import FancyURLopener
from review_classes import browser_opener
from review_classes import MetaItem
from review_classes import MetaReview


reload(sys) 
sys.setdefaultencoding("utf-8")


def format_clean(url, file_name):
    '''
        Clean messy metacritic html into readable xml tree
        Used to determine necessary tags to grab
    '''
    opener = browser_opener()
    pretty = BS(opener.open(url).read()).prettify()
    with open(file_name, 'w') as out:
        out.write(pretty)
 

def get_item_reviews(item_tree, opener):
    '''
        Find all the reviews for a single item on an
        index page, return MetaItem object
    '''

    # --- Item Title ---
    title_div = item_tree.find("div", class_="basic_stat product_title").find("a")
    item_title = title_div.string.strip()
    # Internal link to actual review
    item_link_string = title_div.get("href")

    # --- Artist ---
    artist_div = item_tree.find("li",class_="stat product_artist")
    artist_text = artist_div.find("span", class_="data").get_text().split()

    # --- Meta Score ---
    metascore_div = item_tree.find( "div", 
                                     class_="basic_stat \
                                             product_score \
                                             brief_metascore"
                                    )
    metascore_text = metascore_div.get_text().strip()

    # --- User Average ---
    user_average_div = item_tree.find("li", class_="stat product_avguserscore")
    user_average_text = artist_div.find("span", class_="data").get_text().split()

    # Find Critic Reviews
    critic_link = "http://www.metacritic.com{0}/critic-reviews".format(          
                    item_link_string)
    critic_soup = BS(opener.open(critic_link).read())

    try:
        item_release = critic_soup.find("li", class_="summary_detail release")
        item_release_date = item_release.find("span", class_="data").get_text().split()
    except(AttributeError):
        item_release_date = "None"

    # Initialize meta_item
    meta_item = MetaItem(   title=item_title,
                            artist_name=artist_text,
                            meta_score=metascore_text,
                            user_average=user_average_text,
                            release_date=item_release_date
                            )

    critic_list = critic_soup.find_all("li", class_="review critic_review")

    # Loop through all the critic reviews 
    for critic in critic_list:

        critic_name = critic.find("div",class_="review_critic").get_text().strip()
        critic_score = critic.find("div", class_="review_grade").get_text().strip()
        critic_text = critic.find("div", class_="review_body").get_text().strip()

        try:
            critic_link_container = critic.find("li", class_="review_action full_review").find("a")
            critic_link = critic_link_container.get("href").split("?utm_source")[0]
        except(AttributeError):
            critic_link = "None"

        item_review = MetaReview (  critic=critic_name,
                                    score=critic_score,
                                    text=critic_text,
                                    link=critic_link
                                    )

        # Add review to metacritic item
        meta_item.add_review(item_review)

    return meta_item


def nav_item_tree(opener, item_tree_list, item_dict, item_count):
    '''
        Add reviews from an index page to dictionary
    '''
    # Iterate through reviews in list
    for item_tree in item_tree_list:
        # MetaItem Object of all reviews
        meta_item = get_item_reviews(item_tree, opener)
        # Add MetaItem to dictionary
        item_dict[meta_item.title] = meta_item
        item_review_num = len(meta_item.reviews.keys())
        item_count += item_review_num
        print("Item: {0}, Number of Reviews: {1}".format(meta_item.title, 
                                                        item_review_num
                                                        )
                )
    return item_dict, item_count


def meta_miner(shelf_name, starting_letter=None):
    '''
        Mine Metacritic for all reviews of itemtype
        Store in shelf object, writing at each index page
    '''
    # Start at particular index letter?
    if starting_letter != None:
        starting_number = ord(starting_letter)
        alphbet = [chr(x) for x in range(starting_number,123)]
    else:
        alphbet = [""] + [chr(x) for x in range(97,123)]
 
    # Initialize Agent Opener
    opener = browser_opener()
    # First page of item index
    base_link = "http://www.metacritic.com/browse/albums/artist"  
    item_count = 0
    item_dictionary = {}

    # Loop through all of the letters in the index
    for char in alphbet:

        print("Accessing Index Page: {0}/{1}/...\n\
               \t (Total reviews so far: {2})\n".format(base_link,
                                                        char,
                                                        item_count
                                                        )
               )

        # Open first page of item index ("#" page)
        link = "{0}/{1}".format(base_link,char)
        chr_saurce = opener.open(link).read()
        chr_soup = BS(chr_saurce)
        item_tree_list = chr_soup.find_all("li", class_="product release_product")
        item_dictionary, item_count = nav_item_tree(opener,
                                                    item_tree_list, 
                                                    item_dictionary, 
                                                    item_count
                                                    )
        # Subsequent Pages
        reached_end = False
        page_num = 1

        while (not reached_end):
            print("Accessing Index Page: {0}/{1}/{2}...\n\
                   \t (Total reviews so far: {3})\n".format(base_link,
                                                            char,
                                                            page_num,
                                                            item_count
                                                            )
                   )
            link = "{0}/{1}?page={2}".format(base_link, char, page_num)
            chr_saurce = opener.open(link).read()
            chr_soup = BS(chr_saurce)
            
            # at end yet?
            reached_end = (chr_soup.find("div",class_="error404_module")!=None)

            item_tree_list = chr_soup.find_all("li", class_="product release_product")
            item_dictionary, item_count = nav_item_tree(opener,
                                                        item_tree_list, 
                                                        item_dictionary, 
                                                        item_count
                                                        )

        # Store data after every index page
        print("Shelving Data in \"{0}\"\n").format(shelf_name)
        item_storage = shelve.open(shelf_name)
        item_storage["raw_data"] = item_dictionary
        item_storage.close()

def main():
    meta_miner('raw_data')

if __name__ == "__main__":
    main()
