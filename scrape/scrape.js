//
// scrape a url for data
//


var _ = require('lodash-node'),
    cheerio = require('cheerio'),
    request = require('request');


function getData(selection, data, output) {

  output = output || {};

  function stripField(value, key) {
    var $key = selection.find(key),
        multiple = $key.length > 1;

    if (!value.field) {
      output = getData($key, value, output);
    } else {

      if (value.text) {

        if (multiple) {
          var out = [];
          $key.each(function() {
            out.push(cheerio(this).text())
          })
          output[value.field] = out;
        } else {
          output[value.field] = $key.text()
        }
        
      } else if (value.attr) {

        if (multiple) {
          var out = [];
          $key.each(function() {
            out.push(cheerio(this).attr(value.attr))
          })
          output[value.field] = out;
        } else {
          output[value.field] = $key.attr(value.attr);
        }

      }
      
    }
  }

  _.forEach(data, function(value, key) {
    if (value instanceof Array) {
      _.forEach(value, function(v) {
        stripField(v, key);
      })
    } else {
      stripField(value, key);
    }
  })

  return output;

}


function scrape(url, data, callback) {
  callback = callback || function(e, r) {console.log(r);};
  request(url, function (error, response, body) {
    if (!error && response.statusCode == 200) {
      var $ = cheerio.load(body);
      callback(
        error, 
        getData($('body'), data)
      )
    }
  })
}


module.exports = scrape;
