//
// collect a page of reviews
//

var scrape = require('./scrape.js'),
    album = require('./album.js'),
    queue = require('queue-async');

var grid_data = {
  ".object-grid a" : {'field' : "links", "attr" : 'href'}
}

function page(url, callback) {

  callback = callback || function(e, r) {console.log(r);};

  scrape(url, grid_data, function(error, grid) {
    var q = queue(), output = {};

    grid.links.forEach(function(url) {
      q.defer(album, 'http://pitchfork.com' + url)
    });

    // all reviews scraped
    q.awaitAll(function(error, results) {

      grid.links.forEach(function(url, i) {
        output[url] = results[i];
      })

      callback(error || null, output);

    })

  })

}


module.exports = page;
