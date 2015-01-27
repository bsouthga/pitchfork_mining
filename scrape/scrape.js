//
// scrape a url for data
//


var _ = require('lodash-node'),
    cheerio = require('cheerio'),
    request = require('request');


function get(node, value) {

  var result = {};

  if (value.text) result.text = node.text(); 

  // get all attributes requested,
  // if attributes not passed as array,
  // convert to array
  if (value.attr) {
    (
      value.attr instanceof Array ? 
      value.attr : 
      [value.attr]
    )
    .forEach(function(attr) {
      result[attr] = node.attr(attr);
    })
  }

  return result;
}



function getData(selection, data, output) {

  output = output || {};

  function stripField(value, key) {
    
    var $key = selection.find(key),
        multiple = $key.length > 1,
        out, attr, field;

    if (!$key.length) return null;

    if (!value.field) {
      output = getData($key, value, output);
    } else {

      field = value.field;

      // if the selection returns multiple elements
      // collect data for all returned elements
      if (multiple) {
        var out_list = [];
        $key.each(function() {
          out_list.push(get(cheerio(this), value));
        })
        out = out_list;
      } else {
        var out = get($key, value)
      }

      output[field] = out;

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
    } else {
      callback(error || response, {});
    }
  })
}


module.exports = scrape;
