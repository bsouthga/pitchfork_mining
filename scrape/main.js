// (pitchfork) -> json


var page = require('./page.js'),
    queue = require('queue-async'),
    fs = require('fs'),
    request = require('request');


function collect(i) {

  var url = 'http://pitchfork.com/reviews/albums/' + i + '/';

  request(url, function (error, response, body) {
    if (!error && response.statusCode == 200) {
      page(url, function(error, results) {
        console.log('page ' + i + ' collected...')
        fs.writeFile('../data/page_' + i + '.json', JSON.stringify(results));
      });
      collect(i+1);
    }
  })

}

collect(1);

