# Pitchfork Web Scraping Script
# Ben Southgate
# 10/18/13

import sys, Image, io, shelve
from bs4 import BeautifulSoup as BS
from urllib import FancyURLopener
from review_classes import PitchforkReview
from review_classes import write_data
from review_classes import browser_opener

# Handle funky Unicode band names
reload(sys) 
sys.setdefaultencoding("utf-8")


def get_review(link_BS_object):
    '''
        Get all the review information for an individual link
    '''

    opener = browser_opener()

    # Pull review url and open page
    url = "http://pitchfork.com" + link_BS_object.get('href')
    review_page = BS(opener.open(url).read())

    info = BS(str(review_page.find_all("div", class_="info")[0]))

    # Pull info
    artist   = str(info.find("h1").get_text())
    album    = str(info.find("h2").get_text())
    label    = str(info.find("h3").get_text())

    # Check to see if best new music
    try:
        special    = str(info.find("div", class_="bnm-label").get_text())
    except(AttributeError):
        special    = None

    # Some reviews apparently don't have scores
    try:
        score    = float(info.find("span", class_="score").get_text())
    except(AttributeError):
        score    = None

    # Author and date are in same tag
    try:
        author_date   = str(info.find("h4").get_text()).split(";")
        author, date  = author_date[0], author_date[1]
    except(AttributeError):
        author, date    = None, None

    # Find editorial, remove tabs and new lines
    editorial_string = review_page.find_all("div", class_="editorial")[0]
    editorial_soup   = BS(str(editorial_string))
    editorial_text   = str(editorial_soup.get_text())
    editorial        = editorial_text.replace("\t"," ").replace("\n"," ")

    # Get image
    try:  
        artwork   = BS(str(review_page.find_all("div", class_="artwork")[0]))
        image_url = artwork.find("img")['src']
        image_url_read   = opener.open(image_url)
        image_byte_file  = io.BytesIO(image_url_read.read())

        try:    
            # Try to load image
            image = Image.open(image_byte_file)

            # Get average RGB
            red, green, blue = 0, 0, 0
            num_pixels = float(image.size[0]*image.size[1])

            try:
                for x in range(image.size[0]):
                    for y in range(image.size[1]):
                        pixel = image.getpixel((x,y))
                        red   += pixel[0] / num_pixels
                        green += pixel[1] / num_pixels
                        blue  += pixel[2] / num_pixels
                color_avg = (red, green, blue)

            except(TypeError):
                color_avg = None

        except(IOError):
            color_avg = None

    except(TypeError):
        color_avg, image_url = None, None


    # Show progress of the scraping 
    print("\t\t".join([author, date, str(color_avg), artist, album]))

    return  PitchforkReview(    artist=artist,       
                                album=album,   
                                label=label,  
                                date=date,    
                                score=score,       
                                author=author,  
                                color_avg=color_avg,  
                                imglink=image_url,  
                                reviewlink=url,   
                                special=special,      
                                editorial=editorial 
                                )


def collect(starting_page, shelf, export_data=True):
    '''
        Loop through all album review pages, collecting information on each review 
    '''

    reached_last_page = False
    album_page_num = starting_page
    opener = browser_opener()
    review_dict = {}

    while(not reached_last_page):

        # Where are we?
        print("Album Page\t{0}".format(album_page_num))

        # Open album page (contains links to 20 reviews)
        try:
            albums = opener.open(
                        'http://pitchfork.com/reviews/albums/{0}/'.format(
                            str(album_page_num)
                            )
                        ).read()

        # Encounter 404, we're done
        except(IndexError):
            reached_last_page = True


        # Soupify album page
        rsoup = BS(albums)
        try:
            review_list = BS(   str(rsoup.find_all( "ul", 
                                                    class_ = "object-grid"
                                                   )[0]
                                    )
                                )
            review_links = review_list.find_all("a")
        except(AttributeError):
            reached_last_page = True


        for link in review_links:
            review = get_review(link)
            uid = review.artist + review.album
            review_dict[uid] = review

        if export_data:

            shelf['pitchfork_raw_data{0}'.format(starting_page)] = review_dict

            # Write every 5 pages to a tsv file, as a precaution
            if album_page_num % 5 == 0:
                write_data( review_dict, 
                            "pitchfork_raw_data{0}.tsv".format(starting_page)
                            )

        album_page_num = album_page_num + 1

    # Final .tsv output
    if export_data:
        write_data( review_dict, 
                "pitchfork_raw_data{0}.tsv".format(starting_page)
                )
 

if __name__ == "__main__":
    storage = shelve.open('review_storage')
    collect(1, storage)
    storage.close()


