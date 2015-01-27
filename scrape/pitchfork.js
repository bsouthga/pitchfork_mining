//
// scraping methods for pitchfork reviews
//



var scrape = require('./scrape.js'),
    queue = require('queue-async');



// define structure of data to collect
var review = {
  "ul.review-meta" : {
    ".artwork img" : {"field" : "artwork", "attr" : "src"},
    ".info" : {
      "h1 a" : {"field" : "artist", "text" : true, "attr" : "href"},
      "h2" : {"field" : "album", "text" : true},
      "h3" : {"field" : "label", "text" : true},
      "h4" : {
        "a" : {"field" : "author", "text" : true, "attr" : "href"},
        ".pub-date" : {"field" : "date" , "text" : true}
      }
    }
  }
};



var grid_data = {
  ".object-grid a" : {'field' : "links", "attr" : 'href'}
};


function album(url, callback) {
  scrape(url, review, callback);
}


function page(url, callback) {

  callback = callback || function(e, r) {console.log(r);};

  scrape(url, grid_data, function(error, grid) {
    var q = queue(), output = {};

    grid.links.forEach(function(anchor) {
      q.defer(album, 'http://pitchfork.com' + anchor.href)
    });

    // all reviews scraped
    q.awaitAll(function(error, results) {
      grid.links.forEach(function(anchor, i) {
        output[anchor.href] = results[i];
      })
      callback(error || null, output);
    })

  })

}



module.exports = {page : page, album : album};
