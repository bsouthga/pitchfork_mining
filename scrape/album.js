var scrape = require('./scrape.js');


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
  if (verbose) console.log('collecting data from ' + url);
  scrape(url, review, callback);
}

var verbose = false;
album.verbose = function(value) {
  if (!arguments.length) return verbose;
  verbose = value;
  return album;
}

module.exports = album;

