// (pitchfork) -> json


var pitchfork = require('./pitchfork.js'),
    queue = require('queue-async'),
    fs = require('fs'),
    request = require('request');



function collectPitchfork(i, single) {

  var url = 'http://pitchfork.com/reviews/albums/' + i + '/';

  request(url, function (error, response, body) {
    if (!error && response.statusCode == 200) {
      pitchfork.page(url, function(error, results) {
        fs.writeFile(
          '../data/pitchfork/page_' + i + '.json', 
          JSON.stringify(results), 
          function(err) {
            console.log('page ' + i + ' collected...')
          }
        );
      });
      if (!single) collectPitchfork(i+1);
    }
  })

}

collectPitchfork(1);

