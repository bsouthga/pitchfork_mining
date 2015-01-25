var scrape = require('./scrape.js'),
    cheerio = require('cheerio'),
    request = require('request');


// define structure of data to collect
var review = {
  "ul.review-meta" : {
    ".artwork img" : {"field" : "artwork", "attr" : "src"},
    ".info" : {
      "h1 a" : [
        {"field" : "artist", "text" : true},
        {"field" : "artist-url", "attr" : "href"}
      ],
      "h2" : {"field" : "album", "text" : true},
      "h3" : {"field" : "label", "text" : true},
      "h4" : {
        "a" : [
          {"field" : "author", "text" : true},
          {"field" : "author-link", "attr" : "href"}
        ],
        ".pub-date" : {"field" : "date" , "text" : true}
      }
    }
  }
};


function album(url, callback) {
  scrape(url, review, callback);
}


module.exports = album;

